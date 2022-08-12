#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

import os
import shutil
import subprocess
import sys

root=os.getcwd()
e4d_install = root+'/e4d_dev'
mpirun='/shared/E4D/petsc/arch-linux-c-opt/bin/mpirun'
e4d=root+'/e4d_dev/bin/e4d'
tetgen=root+'/e4d_dev/bin/tetgen'
triangle=root+'/e4d_dev/bin/triangle'
bx=root+'/e4d_dev/bin/bx'
px=root+'/e4d_dev/bin/px'
nproc=7

#modes=['ERT1','ERTAnalytic','ERT2','ERT3']
#modes=modes+['ERT1-IMI','ERT2-IMI','ERT3-IMI']
#modes=modes+['SIP1','SIP2','SIP3']
#modes=modes+['SIP1-IMI','SIP2-IMI','SIP3-IMI']
#modes=modes+['ERTtank1','ERTtank2','ERTtank3']
#modes=modes+['SIPtank1','SIPtank2','SIPtank3']
os.environ['LD_LIBRARY_PATH'] = root+'/e4d_dev/lib'

if not os.path.isdir(root+'/tutorial'):
    process=subprocess.Popen('cp -pr '+e4d_install+'/tutorial '+root,shell=True)
    process.wait()
else:
    process=subprocess.Popen('rm -rf '+root+'/tutorial',shell=True)
    process.wait()

    process=subprocess.Popen('cp -pr '+e4d_install+'/tutorial '+root,shell=True)
    process.wait()
    
if not os.path.isdir(root+'/tutorial_JupyterLab'):
    process=subprocess.Popen('cp -pr '+e4d_install+'/tutorial_JupyterLab '+root,shell=True)
    process.wait()
else:
    process=subprocess.Popen('rm -rf '+root+'/tutorial_JupyterLab',shell=True)
    process.wait()

    process=subprocess.Popen('cp -pr '+e4d_install+'/tutorial_JupyterLab '+root,shell=True)
    process.wait()

def set_globvars_fmm(prefix):
    global cfgfile,nodefile,elefile,trnfile,srvfile_fmm
    global sigfile_fmm,outfile_fmm,invfile_fmm,sigsrv_fmm,dpdfile_fmm
        
    cfgfile=prefix+'.cfg'
    nodefile=prefix+'.1.node'
    elefile=prefix+'.1.ele'
    trnfile=prefix+'.trn'
    srvfile_fmm=prefix+'.srv'
    sigfile_fmm=prefix+'.vel'
    outfile_fmm=prefix+'.out'
    invfile_fmm=prefix+'.inv'
    sigsrv_fmm=prefix+'.vel.srv'
    dpdfile_fmm=prefix+'.dpd'
    return

def set_globvars(prefix):
    global cfgfile,nodefile,elefile,trnfile,srvfile
    global sigfile,outfile,invfile,sigsrv,dpdfile
        
    cfgfile=prefix+'.cfg'
    nodefile=prefix+'.1.node'
    elefile=prefix+'.1.ele'
    trnfile=prefix+'.trn'
    srvfile=prefix+'.srv'
    sigfile=prefix+'.sig'
    outfile=prefix+'.out'
    invfile=prefix+'.inv'
    sigsrv=prefix+'.sig.srv'
    dpdfile=prefix+'.dpd'
    return

def test_case(case):
    if case=='inputs':
        #Check E4D error handling for inputs
        os.chdir(root+'/Req_4.0_ERT3')
        set_globvars('test')
        valid_e4dinp('1.1') #check e4d error handling for e4d.inp format
        valid_cfgfile('1.2') #check e4d error handling for mesh configuration file
        valid_mshfile('1.3') #check e4d error handling for mesh node/element file
        valid_srvfile('1.4') #check e4d error handling for survey file
        valid_sigfile('1.5') #check e4d error handling for conductivity file
        
        os.chdir(root+'/Req_4.0_FMM3')
        set_globvars_fmm('test_fmm')
        valid_fmminp('1.6')
        valid_mshfile_fmm('1.7')
        valid_srvfile_fmm('1.8')
        valid_sigfile_fmm('1.9')
        
    elif case=='mesh':
        #Check requirements for TetGen version
        os.chdir(root+'/Req_2.0_TetGen')
        set_globvars('200EW_T')
        valid_tetgen('2.0')
        
        #Check requirements for ERT-mesh
        os.chdir(root+'/Req_2.0_ERT1')
        set_globvars('two_blocks')
        
        valid_mshout('2.1')
        valid_mshlog('2.2')
        valid_poly2d('2.3')
        valid_poly3d('2.4')
        valid_mshqual('2.5')
        
        #Check requirements for ERT_IMI-mesh
        os.chdir(root+'/Req_2.0_ERT1-IMI')
        set_globvars('mbsl')
        
        valid_mshout('2.6.1')
        valid_mshlog('2.6.2')
        valid_poly2d('2.6.3')
        valid_poly3d('2.6.4')
        valid_mshqual('2.6.5')
        valid_iminodes('2.6.6')
        sort_folders('Req_2.6')
        
        #Check requirements for SIP-mesh
        os.chdir(root+'/Req_2.0_SIP1')
        set_globvars('two_blocks')
        
        valid_mshout('2.7.1')
        valid_mshlog('2.7.2')
        valid_poly2d('2.7.3')
        valid_poly3d('2.7.4')
        valid_mshqual('2.7.5')
        valid_sipsig('2.7.6')
        sort_folders('Req_2.7')
        
        #Check requirements for ERT_Tank-mesh
        os.chdir(root+'/Req_2.0_ERTtank1')
        set_globvars('tank')
        
        valid_mshout('2.8.1')
        valid_mshlog('2.8.2')
        valid_poly2d('2.8.3')
        valid_poly3d('2.8.4')
        valid_mshqual('2.8.5')
        sort_folders('Req_2.8')
        
        #Check requirements for SIP_Tank-mesh
        os.chdir(root+'/Req_2.0_SIPtank1')
        set_globvars('tank')
        
        valid_mshout('2.9.1')
        valid_mshlog('2.9.2')
        valid_poly2d('2.9.3')
        valid_poly3d('2.9.4')
        valid_mshqual('2.9.5')
        valid_sipsig('2.9.6')
        sort_folders('Req_2.9')
        
    elif case=='forward':
        #Check requirements for ERT_Analytic-forward
        os.chdir(root+'/Req_3.0_ERTAnalytic')
        set_globvars('two_blocks')
        valid_anout('3.1')
        valid_ansol('3.2')
        
        #Check requirements for ERT-forward
        os.chdir(root+'/Req_3.0_ERT2')
        set_globvars('two_blocks')
        valid_numout('3.3')
        valid_numsol('3.4')
        valid_nproc('3.5')
        
        #Check requirements for ERT_IMI-forward
        os.chdir(root+'/Req_3.0_ERT2-IMI')
        set_globvars('mbsl')
        valid_numout('3.6.1')
        sort_folders('Req_3.6')
        
        #Check requiremetns for SIP-forward
        os.chdir(root+'/Req_3.0_SIP2')
        set_globvars('two_blocks')
        valid_numout('3.7.1')
        valid_sipdpd('3.7.2')
        sort_folders('Req_3.7')
        
        #Check requirements for SIP_IMI-forward
        os.chdir(root+'/Req_3.0_SIP2-IMI')
        set_globvars('mbsl')
        valid_numout('3.8.1')
        valid_sipdpd('3.8.2')
        sort_folders('Req_3.8')

        #Check requirements for ERT_Tank-forward
        os.chdir(root+'/Req_3.0_ERTtank2')
        set_globvars('tank')
        valid_numout('3.9.1')
        sort_folders('Req_3.9')

        #Check requirements for SIP_Tank-forward
        os.chdir(root+'/Req_3.0_SIPtank2')
        set_globvars('tank')
        valid_numout('3.10.1')
        valid_sipdpd('3.10.2')
        sort_folders('Req_3.10')
        
        #Check requirements for  FMM-forward
        os.chdir(root+'/Req_3.0_FMM2')
        set_globvars_fmm('borehole')
        valid_numout_fmm('3.11.1')
        sort_folders('Req_3.11')
        
    elif case=='inversion':
        #Check requirements for ERT-inversion
        os.chdir(root+'/Req_4.0_ERT3')
        set_globvars('two_blocks')
        valid_invfile('4.1')
        valid_invout('4.2')
        valid_misfit('4.3')
        valid_nproc('4.4')
        
        #Check requirements for ERT_TL-inversion (TL: time-lapse)
        os.chdir(root+'/Req_4.0_ERT4')
        set_globvars('sp')
        valid_tlsrv('4.5.1')
        valid_tlout('4.5.2')
        sort_folders('Req_4.5')
        
        #Check requirements for ERT_IMI-inversion
        os.chdir(root+'/Req_4.0_ERT3-IMI')
        set_globvars('mbsl')
        valid_invout('4.6.1')
        valid_misfit('4.6.2')
        sort_folders('Req_4.6')
        
        #Check requirements for FMM-inversion
        os.chdir(root+'/Req_4.0_FMM3')
        set_globvars_fmm('borehole')
        valid_invout_fmm('4.7.1')
        valid_misfit_fmm('4.7.2')
        sort_folders('Req_4.7')
    
    elif case=='px':
        #Check requirements for px command line input
        print(root+'/Req_5.1')
        if not os.path.isdir(root+'/Req_5.1'):
            print('True')
            process=subprocess.Popen('cp -pr include/px '+root+'/Req_5.1',shell=True)
            process.wait()
        else:
            process=subprocess.Popen('rm -rf '+root+'/Req_5.1',shell=True)
            process.wait()
            
            process=subprocess.Popen('cp -pr include/px '+root+'/Req_5.1',shell=True)
            process.wait()
            
        os.chdir(root+'/Req_5.1')
        valid_px_input('5.1.1')
        valid_px_ids('5.1.2')
        valid_px_varname('5.1.3')
        
    return

def valid_px_input(tag):
    with open('run.log','w') as f:
        process=subprocess.Popen([px+' -f two_blocks two_blocks.sig test'],stdout=f,shell=True)
        process.wait()
    
    msg='Requirement %s: Check if all input variables were entered at the command line'%(tag)
    print('')
    print_splitter('Test Px Input','=',80)
    print(msg)
    
    with open('run.log','r') as f:
        if 'Not enough input variables entered' in f.read():
            print('Success: px reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by px')
            sys.stderr.write(msg+'\npx failed to report error\n')
    return

def valid_px_ids(tag):
    cnt=-1
    # create element xmf/h5 file
    with open('run.log','w') as f:
        process=subprocess.Popen([px+' -f two_blocks two_blocks.sig test 0'],stdout=f,shell=True)
        process.wait()
    
    # check recognition of filetype
    # element file
    cnt+=1
    msg='Requirement %s.%d: Check if element file type is indicated'%(tag,cnt)
    print('')
    print_splitter('Test Px Input','=',80)
    print(msg)
    
    with open('run.log','r') as f:
        if 'element' in f.read():
            print('Success: px recognized element file')
        else:
            print ('Failed: px did not recognized element file type')
            sys.stderr.write(msg+'Failed: px did not recognized element file type')
    
    # node file
    cnt+=1
    msg='Requirement %s.%d: Check if node file type is indicated'%(tag,cnt)
    print('')
    print_splitter('Test Px Input','=',80)
    print(msg)
    
    with open('run.log','w') as f:
        process=subprocess.Popen([px+' -f two_blocks potential.1849 test2 0'],stdout=f, shell=True)
        process.wait()
    
    with open('run.log','r') as f:        
        if 'node' in f.read():
            print('Success: px recognized node file')
        else:
            print ('Failed: px did not recognized node file type')
            sys.stderr.write(msg+'\npx did not recognize node file type')
    
    
    # add file to existing visualization file
    cnt+=1
    msg='Requirement %s.%d: Check if duplicate time stamp is detected from command line input'%(tag,cnt)
    print('')
    print_splitter('Test Px Input','=',80)
    print(msg)
    
    with open('run.log','w') as f:
        process=subprocess.Popen([px+' -af two_blocks two_blocks.sig test 0'],stdout=f,shell=True)
        process.wait()
    
    with open('run.log','r') as f:
        if 'The time stamp definition has already been defined' in f.read():
            print('Success: px reported error and exited cleanly')
        else:
            print('Error: px did not exit cleanly when time stamp was reused')
            sys.stderr.write(msg+'\npx failed to exit cleanly.\n')
    return

def valid_px_varname(tag):
    with open('run.log','w') as f:
        process=subprocess.Popen([px+' -f two_blocks two_blocks.sig test 0 var1'],stdout=f,shell=True)
        process.wait()
    
    msg='Requirement %s: Check if variable name is detected from command line input'%(tag)
    print('')
    print_splitter('Test Px Input','=',80)
    print(msg)
    
    with open('run.log','r') as f:
        if 'Variable name entered:' in f.read():
            print('Success: px recognized variable name entry')
        else:
            print('Failed: px did not recognize variable name entry')
            sys.stderr.write(msg+'\npx failed to recognize variable name entry\n')
    
    return

def valid_tlsrv(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    mycopyfile('e4d.inp','e4d_copy.inp')
    mycopyfile('e4d.log','e4d_copy.log')
    mycopyfile('run.log','run_copy.log')
    mycopyfile('surveys.txt','surveys_copy.txt')
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if the time-lapse survey list file exists'%(tag,cnt)+\
    '\n... Cannot find the time lapse survey list file: surveys.txt'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    myremove('surveys.txt')
    
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'Cannot find the time lapse survey list file: surveys.txt' in f.read():
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
            
    #mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    #mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    #mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    #mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check time-lapse survey list file format'%(tag,cnt)+\
    '\n... There was a problem reading the number of survey files in surveys.txt'
    print('')
    print_splitter('Testing E4D Error handling','=',80)
    print(msg)
    
    with open('surveys.txt','w') as f:
        f.write('')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading the number of survey files in surveys.txt' in f.read():
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile('surveys.txt',wdir+'/Req_%s.%d/surveys.txt'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check time-lapse survey list file format'%(tag,cnt)+\
    '\n... There was a problem reading time-lapse file at time            1'+\
    '\n... in the time lapse survey file: surveys.txt'
    print('')
    print_splitter('Testing E4D Error handling','=',80)
    print(msg)
    
    with open('surveys.txt','w') as f:
        f.write('3\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading time-lapse file at time            1'+\
        ' in the time lapse survey file: surveys.txt' in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile('surveys.txt',wdir+'/Req_%s.%d/surveys.txt'%(tag,cnt))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check time-lapse survey list file format'%(tag,cnt)+\
    '\n... There was a problem finding the time-lapse file: sig_0.0.srv'
    print('')
    print_splitter('Testing E4D Error handling','=',80)
    print(msg)
    
    with open('surveys.txt','w') as f:
        f.write('3\n')
        f.write('sig_0.0.srv 0.0\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem finding the time-lapse file: sig_0.0.srv' in f.read():
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile('surveys.txt',wdir+'/Req_%s.%d/surveys.txt'%(tag,cnt))

    mymove('e4d_copy.inp','e4d.inp')
    mymove('e4d_copy.log','e4d.log')
    mymove('run_copy.log','run.log')
    mymove('surveys_copy.txt','surveys.txt')
    return

def valid_tlout(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
        
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if E4D runs'%(tag,cnt)
    print('')
    print_splitter('Test Inversion Mode','=',80)
    print(msg)
    
    if os.path.isfile('e4d.log'):
        print('Success: e4d.log was found')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
        return

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if tl_sig*.* exists'%(tag,cnt)
    print('')
    print_splitter('Test Inversion Mode','=',80)
    print(msg)
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    with open('surveys.txt') as f:
        nt=int(f.readline().split()[0])
        flist=[]
        times=[]
        for line in f:
            flist.append(line.split()[0])
            times.append(float(line.split()[1]))
    
    for i in range(nt):
        fname='tl_sig%.3f'%times[i]
        if not os.path.isfile(fname):
            break
        else:
            mycopyfile(fname,wdir+'/Req_%s.%d/%s'%(tag,cnt,fname))
    
    if i==nt-1:
        print('Success: Conductivity files tl_sig%.3f to tl_sig%.3f were found'%(times[0],times[-1]))
    else:
        print('Failed: Time-lapse inversion was not ran sucessfully')
        sys.stderr.write(msg+'\nTime-lapse inversion failed\n')
    
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    return

def valid_tetgen(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if E4D runs'%(tag,cnt)
    print('')
    print_splitter('Validate TetGen Version','=',80)
    print(msg)

    if os.path.isfile('e4d.log'):
        print('Success: e4d.log was found')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
        return

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if E4D runs'%(tag,cnt)
    print('')
    print_splitter('Validate TetGen Version','=',80)
    print(msg)

    if os.path.isfile('check.txt'):
        print('Success: check.txt was found')
    else:
        print('Failed: TetGen Version Validation was not ran successfully')
        sys.stderr.write(msg+'\nTetGen Version Validation failed\n')
        return

    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    mycopyfile(elefile+'.standard',wdir+'/Req_%s.%d/%s.standard'%(tag,cnt,cfgfile))
    mycopyfile('check.txt',wdir+'/Req_%s.%d/check.txt'%(tag,cnt))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if %s is identical to %s.standard'%(tag,cnt,elefile,elefile)
    print('')
    print_splitter('Validate TetGen Version','=',80)
    print(msg)
    
    with open('check.txt') as f:
        lines=f.readlines()

    if not lines:
        print('Success: TetGen version test passed')
    else:
        print('Failed: TetGen version test failed')
        sys.stderr.write(msg+'\nTetGen version test failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    mycopyfile(elefile+'.standard',wdir+'/Req_%s.%d/%s.standard'%(tag,cnt,cfgfile))
    mycopyfile('check.txt',wdir+'/Req_%s.%d/check.txt'%(tag,cnt))

    return

def valid_mshout(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
        
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if E4D runs'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)

    if os.path.isfile('e4d.log'):
        print('Success: e4d.log was found')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
        return

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if mesh_build.log exists'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)

    if os.path.isfile('mesh_build.log'):
        print('Success: mesh_build.log was found')
    else:
        print('Failed: Mesh was not generated successfully')
        sys.stderr.write(msg+'\nMesh generation failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    mycopyfile('mesh_build.log',wdir+'/Req_%s.%d/mesh_build.log'%(tag,cnt))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if surface.poly exists'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)

    if os.path.isfile('surface.poly'):
        print('Success: surface.poly was found')
    else:
        print('Failed: Mesh was not generated successfully')
        sys.stderr.write(msg+'\nMesh generation failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    mycopyfile('surface.poly',wdir+'/Req_%s.%d/surface.poly'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    polyfile=cfgfile.split('.')[0]+'.poly'
    msg='Requirement %s.%d: Check if %s exists'%(tag,cnt,polyfile)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)

    if os.path.isfile(polyfile):
        print('Success: %s was found'%polyfile)
    else:
        print('Failed: Mesh was not generated successfully')
        sys.stderr.write(msg+'\nMesh generation failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    mycopyfile(polyfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,polyfile))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if tetgen output files exist'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    prefix=cfgfile.split('.')[0]
    flist=[prefix+'.1.node',prefix+'.1.ele',prefix+'.1.neigh',prefix+'.1.edge',prefix+'.1.face',prefix+'.trn']
    for file in flist:
        if os.path.isfile(file):
            print('Success: %s was found'%file)
        else:
            print('Failed: Mesh was not generated successfully')
            sys.stderr.write(msg+'\nMesh generation failed\n')
        mycopyfile(file,wdir+'/Req_%s.%d/%s'%(tag,cnt,file))

    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))

    #====================================================================================================
    cnt=cnt+1
    if bx.split('/')[-1]=='px':
        h5=cfgfile.split('.')[0]+'.h5'
        xmf=cfgfile.split('.')[0]+'.xmf'
        msg='Requirement %s.%d: Check if %s and %s exist'%(tag,cnt,h5,xmf)
        print('')
        print_splitter('Test Mesh Generation Mode','=',80)
        print(msg)
        
        if os.path.isfile(h5):
            print('Success: %s was found'%h5)
        else:
            print('Failed: Px was not ran successfully')
            sys.stderr.write(msg+'\nPx failed to generate mesh visualization file(s)\n')
        
        if os.path.isfile(xmf):
            print('Success: %s was found'%xmf)
        else:
            print('Failed: Px was not ran successfully')
            sys.stderr.write(msg+'\nPx failed to generate mesh visualization file(s)\n')
        
        mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
        mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
        mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
        mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
        mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
        mycopyfile(h5,wdir+'/Req_%s.%d/%s'%(tag,cnt,h5))
        mycopyfile(xmf,wdir+'/Req_%s.%d/%s'%(tag,cnt,xmf))
        
    else:
        exofile=cfgfile.split('.')[0]+'.exo'
        msg='Requirement %s.%d: Check if %s exists'%(tag,cnt,exofile)
        print('')
        print_splitter('Test Mesh Generation Mode','=',80)
        print(msg)

        if os.path.isfile(exofile):
            print('Success: %s was found'%exofile)
        else:
            print('Failed: Bx was not ran successfully')
            sys.stderr.write(msg+'\nBx failed to generate mesh visualization file\n')
    
        mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
        mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
        mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
        mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
        mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
        mycopyfile(exofile,wdir+'/Req_%s.%d/%s'%(tag,cnt,exofile))
        
    return

def valid_mshlog(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
        
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if mesh_build.log exists'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)

    if os.path.isfile('mesh_build.log'):
        print('Success: mesh_build.log was found')
    else:
        print('Failed: Mesh was not generated successfully')
        sys.stderr.write(msg+'\nMesh generation failed\n')
        return
    
    #====================================================================================================
    get_mshcfg(cfgfile)
    with open('mesh_build.log','r') as f:
        for line in f:
            if len(line.split())==0:
                continue

            if 'Allocating arrays' in line:
                ncpts2=int(line.split()[3])
                cpts2=np.zeros((ncpts2,5))
            elif 'Control point' in line:
                index=int(line.split()[2])
                cpts2[index-1,0]=float(line.split()[4])
                cpts2[index-1,1]=float(line.split()[5])
                cpts2[index-1,2]=float(line.split()[6])
                cpts2[index-1,3]=float(line.split()[7])
                cpts2[index-1,4]=int(line.split()[8])
            elif 'piecewise linear complexes' in line:
                nplc2=int(line.split()[2])
                plc2=np.zeros((nplc2,2))
            elif 'boundary number' in line:
                index=int(line.split()[8])
                plc2[index-1,0]=int(line.split()[10])
                plc2[index-1,1]=int(line.split()[11])
            elif 'holes' in line:
                nholes2=int(line.split()[2])
                holes2=np.zeros((nholes2,4))
            elif 'Coordinates for hole' in line:
                index=int(line.split()[3])
                holes2[index-1,0]=index
                holes2[index-1,1]=float(line.split()[5])
                holes2[index-1,2]=float(line.split()[6])
                holes2[index-1,3]=float(line.split()[7])
            elif 'zones' in line:
                nzones2=int(line.split()[2])
                zones2=np.zeros((nzones2,7))
            elif 'Config info for zone' in line:
                index=int(line.split()[4])
            elif 'Zone Number' in line:
                zones2[index-1,0]=int(line.split()[2])
            elif 'Point in zone' in line:
                zones2[index-1,1]=float(line.split()[3])
                zones2[index-1,2]=float(line.split()[4])
                zones2[index-1,3]=float(line.split()[5])
            elif 'Maximum volume' in line:
                zones2[index-1,4]=float(line.split()[2])
            elif 'Complex Conductivity' in line:
                zones2[index-1,6]=float(line.split()[2])
            elif 'Conductivity' in line:
                zones2[index-1,5]=float(line.split()[1])
    
    cnt=cnt+1
    msg='Requirement %s.%d: Check control points in mesh_build.log'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if ncpts>0:
        if ncpts==ncpts2 and all(isclose(cpts,cpts2)):
            print('Success: Control points in mesh_build.log and %s matched'%cfgfile)
        else:
            print('Failed: Control points in mesh_build.log and %s did not match'%cfgfile)
            sys.stderr.write(msg+'\nMesh generation failed\n')
    else:
        print('Number of control points is zero. Skipping')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile('mesh_build.log',wdir+'/Req_%s.%d/mesh_build.log'%(tag,cnt))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check PLC configuration in mesh_build.log'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if nplc>0:
        if nplc==nplc2 and all(isclose(plc,plc2)):
            print('Success: PLC configuration in mesh_build.log and %s matched'%cfgfile)
        else:
            print('Failed: PLC configuration in mesh_build.log and %s did not match'%cfgfile)
            sys.stderr.write(msg+'\nMesh generation failed\n')
    else:
        print('Number of PLC is zero. Skipping')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile('mesh_build.log',wdir+'/Req_%s.%d/mesh_build.log'%(tag,cnt))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check hole configuration in mesh_build.log'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if nholes>0:
        if nholes==nholes2 and all(isclose(holes[:,1:],holes2[:,1:])):
            print('Success: Hole configuration in mesh_build.log and %s matched'%cfgfile)
        else:
            print('Failed: Hole configuration in mesh_build.log and %s did not match'%cfgfile)
            sys.stderr.write(msg+'\nMesh generation failed\n')
    else:
        print('Number of holes is zero. Skipping')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile('mesh_build.log',wdir+'/Req_%s.%d/mesh_build.log'%(tag,cnt))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check zone configuration in mesh_build.log'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if nzones>0:
        if nzones==nzones2 and all(isclose(zones,zones2)):
            print('Success: Zone configuration in mesh_build.log and %s matched'%cfgfile)
        else:
            print('Failed: Zone configuration in mesh_build.log and %s did not match'%cfgfile)
            sys.stderr.write(msg+'\nMesh generation failed\n')
    else:
        print('Number of zones is zero. Skipping')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile('mesh_build.log',wdir+'/Req_%s.%d/mesh_build.log'%(tag,cnt))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))

    return

def valid_poly2d(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if surface.poly exists'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)

    if os.path.isfile('surface.poly'):
        print('Success: surface.poly was found')
    else:
        print('Failed: Mesh was not generated successfully')
        sys.stderr.write(msg+'\nMesh generation failed\n')
        return
    
    #====================================================================================================
    get_mshcfg(cfgfile)
    #trnfile=cfgfile.split('.')[0]+'.trn'
    #if os.path.isfile(trnfile):
    #    trn=np.loadtxt(trnfile)
    #else:
    #    trn=np.zeros(3)
    with open('surface.poly') as f:
        for line in f:
            if len(line.split())==0:
                continue

            if 'Total nodes' in line:
                nnodes=int(line.split()[0])
                nodes=np.zeros((nnodes,4))
                nodcnt=0
            elif '#' in line:
                continue
            elif nodcnt<nnodes:
                nodes[nodcnt,0]=int(line.split()[0])
                nodes[nodcnt,1]=float(line.split()[1])
                nodes[nodcnt,2]=float(line.split()[2])
                nodes[nodcnt,3]=int(line.split()[3])
                nodcnt=nodcnt+1
    
    mask=cpts[:,-1]==1
    surfcpts=cpts[mask,1:3]
    mask=cpts[:,-1]==2
    sbndcpts=cpts[mask,1:3]

    mask=nodes[:,-1]==1
    surfnodes=nodes[mask,1:3]
    mask=nodes[:,-1]==2
    sbndnodes=nodes[mask,1:3]

    cnt=cnt+1
    msg='Requirement %s.%d: Check surface points in surface.poly'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)

    if len(surfcpts)==len(surfnodes) and all(isclose(surfcpts,surfnodes)):
        print('Success: Surface points in surface.poly and %s matched'%cfgfile)
    else:
        print('Failed: Surface points in surface.poly and %s did not match'%cfgfile)
        sys.stderr.write(msg+'\nMesh generation failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile('surface.poly',wdir+'/Req_%s.%d/surface.poly'%(tag,cnt))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check surface outer boundaries in surface.poly'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if len(sbndcpts)==len(sbndnodes) and all(isclose(sbndcpts,sbndnodes)):
        print('Success: Surface outer boundaries in surface.poly and %s matched'%cfgfile)
    else:
        print('Failed: Surface outer boundaries in surface.poly and %s did not matched'%cfgfile)
        sys.stderr.write(msg+'\nMesh generation failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile('surface.poly',wdir+'/Req_%s.%d/surface.poly'%(tag,cnt))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))

    return

def valid_poly3d(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    #====================================================================================================
    cnt=cnt+1
    polyfile=cfgfile.split('.')[0]+'.poly'
    msg='Requirement %s.%d: Check if %s exists'%(tag,cnt,polyfile)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)

    if os.path.isfile(polyfile):
        print('Success: %s was found'%polyfile)
    else:
        print('Failed: Mesh was not generated successfully')
        sys.stderr.write(msg+'\nMesh generation failed\n')
        return
    
    #====================================================================================================
    get_mshcfg(cfgfile)
    trnfile=cfgfile.split('.')[0]+'.trn'
    if os.path.isfile(trnfile):
        trn=np.loadtxt(trnfile)
    else:
        trn=np.zeros(3)
    lincnt=0
    with open(polyfile) as f:
        for line in f:
            if len(line.split())==0:
                continue
            lincnt=lincnt+1

            if 'Total nodes' in line:
                nnodes=int(line.split(',')[0])
                nodes=np.zeros((nnodes,5))
                nodcnt=0
            elif 'points contains the surface points' in line:
                nnsurf=int(line.split()[3])
            elif 'points define the lower boundary' in line:
                nnlbnd=int(line.split()[3])
            elif 'points are internal refine points' in line:
                nnint=int(line.split()[3])
            elif 'Total number of facets' in line:
                nfacets=int(line.split()[0])
                facets=np.zeros((nfacets,2))
                facetlist=[]
                faccnt=0
            elif 'facets define the surface' in line:
                nfsurf=int(line.split()[3])
            elif 'facets define the vertical boundaries' in line:
                nfvert=int(line.split()[3])
            elif 'facet defines the lower boundary' in line:
                nflbnd=1
            elif 'USER DEFINED PLC' in line:
                nfplc=int(line.split()[1])
            elif 'Number of holes' in line:
                nholes2=int(line.split()[0])
                holes2=np.zeros((nholes2,4))
                holcnt=0
            elif 'Number of zones' in line:
                nzones2=int(line.split()[0])
                zones2=np.zeros((nzones2,5))
                zoncnt=0
            elif  '#' in line:
                continue
            elif nodcnt>=0 and nodcnt<nnodes:
                nodes[nodcnt,0]=int(line.split()[0])
                nodes[nodcnt,1]=float(line.split()[1])+trn[0]
                nodes[nodcnt,2]=float(line.split()[2])+trn[1]
                nodes[nodcnt,3]=float(line.split()[3])+trn[2]
                nodes[nodcnt,4]=int(line.split()[5])
                nodcnt=nodcnt+1
            elif faccnt>=0 and faccnt<nfacets*2:
                if (faccnt+1)%2:
                    facets[int(faccnt/2),1]=int(line.split()[2])
                else:
                    facets[int(faccnt/2),0]=len(line.split())
                    facetlist.append(np.array([int(s) for s in line.split()]))
                faccnt=faccnt+1
            elif holcnt>=0 and holcnt<nholes2:
                holes2[holcnt,0]=int(line.split()[0])
                holes2[holcnt,1]=float(line.split()[1])+trn[0]
                holes2[holcnt,2]=float(line.split()[2])+trn[1]
                holes2[holcnt,3]=float(line.split()[3])+trn[2]
                holcnt=holcnt+1
            elif zoncnt>=0 and zoncnt<nzones2:
                zones2[zoncnt,0]=int(line.split()[0])
                zones2[zoncnt,1]=float(line.split()[1])+trn[0]
                zones2[zoncnt,2]=float(line.split()[2])+trn[1]
                zones2[zoncnt,3]=float(line.split()[3])+trn[2]
                zones2[zoncnt,4]=float(line.split()[5])
                zoncnt=zoncnt+1
                
    mask=cpts[:,-1]==1
    surfcpts=cpts[mask,1:]
    mask=cpts[:,-1]==2
    sbndcpts=cpts[mask,1:]
    mask=(cpts[:,-1]!=1)&(cpts[:,-1]!=2)
    intcpts=cpts[mask,1:]
    
    mask=nodes[:len(surfcpts)+len(sbndcpts),-1]==1
    surfnodes=nodes[:len(surfcpts)+len(sbndcpts),1:][mask]
    mask=nodes[:len(surfcpts)+len(sbndcpts),-1]==2
    sbndnodes=nodes[:len(surfcpts)+len(sbndcpts),1:][mask]
    lbndnodes=nodes[nnsurf:nnsurf+nnlbnd,1:]
    intnodes=nodes[nnsurf+nnlbnd:,1:]
        
    cnt=cnt+1
    msg='Requirement %s.%d: Check surface points in %s'%(tag,cnt,polyfile)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if len(surfcpts)==len(surfnodes) and all(isclose(surfcpts,surfnodes)):
        print('Success: Surface points in %s and %s matched'%(polyfile,cfgfile))
    else:
        print('Failed: Surface points in %s and %s did not match'%(polyfile,cfgfile))
        sys.stderr.write(msg+'\nMesh generation failed\n')

    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(polyfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,polyfile))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check surface outer boundaries in %s'%(tag,cnt,polyfile)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if len(sbndcpts)==len(sbndnodes) and all(isclose(sbndcpts,sbndnodes)):
        print('Success: Surface outer boundaries in %s and %s matched'%(polyfile,cfgfile))
    else:
        print('Failed: Surface outer boundaries in %s and %s matched'%(polyfile,cfgfile))
        sys.stderr.write(msg+'\nMesh generation failed\n')

    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(polyfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,polyfile))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check lower boundary in %s'%(tag,cnt,polyfile)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if all(isclose(mbot,lbndnodes[:,2])) and not any(lbndnodes[:,-1].astype(int)-2):
        print('Success: Lower boundary in %s and %s matched'%(polyfile,cfgfile))
    else:
        print('Failed: Lower boundary in %s and %s did not match'%(polyfile,cfgfile))
        sys.stderr.write(msg+'\nMesh generation failed\n')

    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(polyfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,polyfile))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check internal refine points and flags (zero and/or negative) in %s'%(tag,cnt,polyfile)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if len(intcpts)==len(intnodes) and all(isclose(intcpts,intnodes)):
        print('Success: Internal refine points in %s and %s matched'%(polyfile,cfgfile))
    else:
        print('Failed: Internal refine points in %s and %s did not match'%(polyfile,cfgfile))
        sys.stderr.write(msg+'\nMesh generation failed\n')

    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(polyfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,polyfile))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check surface boundary flag in %s'%(tag,cnt,polyfile)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if not any(facets[:nfsurf,-1].astype(int)-1):
        print('Success: Surface boundary flag was set to 1 in %s'%polyfile)
    else:
        print('Failed: At least one surface boundary flag was not 1 in %s'%polyfile)
        sys.stderr.write(msg+'\nMesh generation failed\n')

    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(polyfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,polyfile))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check side and bottom flag in %s'%(tag,cnt,polyfile)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if not any(facets[nfsurf:nfsurf+nfvert+1,-1].astype(int)-2):
        print('Success: Side and bottom boundary flag was set to 2 in %s'%polyfile)
    else:
        print('Failed: At least one side and bottom boundary flag was not set to 2 in %s'%polyfile)
        sys.stderr.write(msg+'\nMesh generation failed\n')

    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(polyfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,polyfile))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inner boundary flag in %s'%(tag,cnt,polyfile)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if nplc>0:
        if nfplc==nplc and not any(facets[nfsurf+nfvert+1:,1]-plc[:,1]):
            print('Success: Inner boundary flag in %s and %s matched'%(polyfile,cfgfile))
        else:
            print('Failed: Inner boundary flag in %s and %s did not match'%(polyfile,cfgfile))
            sys.stderr.write(msg+'\nMesh generation failed\n')
    else:
        print('Number of PLC is zero. Skipping')

    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(polyfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,polyfile))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check PLC points in %s'%(tag,cnt,polyfile)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if nplc>0:
        passed=True
        for i in range(nplc):
            plccpts=cpts[plclist[i].astype(int)-1,1:4]
            plcnodes=nodes[facetlist[nfsurf+nfvert+1:][i].astype(int)-1,1:4]
            for j in range(len(plccpts)):
                xmatch=isclose(plccpts[j,0],plcnodes[:,0])
                ymatch=isclose(plccpts[j,1],plcnodes[:,1])
                zmatch=isclose(plccpts[j,2],plcnodes[:,2])
                if not any(xmatch&ymatch&zmatch):
                    passed=False
                    break

        if passed:
            print('Success: PLC points in %s and %s matched'%(polyfile,cfgfile))
        else:
            print('Failed: PLC points in %s and %s did not match'%(polyfile,cfgfile))
            sys.stderr.write(msg+'\nMesh generation failed\n')
    else:
        print('Number of PLC is zero. Skipping')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(polyfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,polyfile))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check hole configuration in %s'%(tag,cnt,polyfile)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if nholes>0:
        if nholes==nholes2 and all(isclose(holes[:,1:],holes2[:,1:])):
            print('Success: Hole configuration in %s and %s matched'%(polyfile,cfgfile))
        else:
            print('Failed: Hole configuration in %s and %s did not match'%(polyfile,cfgfile))
            sys.stderr.write(msg+'\nMesh generation failed\n')
    else:
        print('Number of holes is zero. Skipping')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(polyfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,polyfile))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check zone configuration in %s'%(tag,cnt,polyfile)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    if nzones>0:
        if nzones==nzones2 and all(isclose(zones[:,:-2],zones2)):
            print('Success: Zone configuration in %s and %s matched'%(polyfile,cfgfile))
        else:
            print('Failed: Zone configuration in %s and %s did not match'%(polyfile,cfgfile))
            sys.stderr.write(msg+'\nMesh generation failed\n')
    else:
        print('Number of zones is zero. Skipping')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(polyfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,polyfile))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    
    return

def valid_mshqual(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
        
    with open('test_mqual.cfg','w') as f:
        f.write('1.8 1e12\n')
        with open(cfgfile,'r') as f_old:
            f_old.readline()
            f.write(f_old.read())
    
    #with open('e4d.inp','w') as f:
    #    f.write('ERT1\n')
    #    f.write('test_mqual.cfg\n')
    replace_line('e4d.inp',cfgfile,'test_mqual.cfg')
    
    print('')
    print('[Running mode 1] mpirun -np %d e4d'%nproc)
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if all the mesh files exist'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    prefix=cfgfile.split('.')[0]
    flist=[prefix+'.1.node',prefix+'.1.ele',prefix+'.1.neigh',prefix+'.1.edge',prefix+'.1.face',prefix+'.trn']
    for file in flist:
        if os.path.isfile(file):
            print('Success: %s was found'%file)
        else:
            print('Failed: Old mesh files were not found')
            sys.stderr.write(msg+'\nMesh quality test failed\n')
            return
    
    prefix='test_mqual'
    flist=[prefix+'.1.node',prefix+'.1.ele',prefix+'.1.neigh',prefix+'.1.edge',prefix+'.1.face',prefix+'.trn']
    for file in flist:
        if os.path.isfile(file):
            print('Success: %s was found'%file)
        else:
            print('Failed: New mesh files were not found')
            sys.stderr.write(msg+'\nMesh quality test failed\n')
            return
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if the mesh quality number affects the mesh elements'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode','=',80)
    print(msg)
    
    elefile=cfgfile.split('.')[0]+'.1.ele'
    with open(elefile) as f:
        nele = int(f.readline().split()[0])
    
    with open('test_mqual.1.ele') as f:
        nele2 = int(f.readline().split()[0])
    
    if nele!=nele2:
        print('Success: The number of mesh elements changed with the mesh quality number')
    else:
        print('Failed: The number of mesh elements did not change with the mesh quality number')
        sys.stderr.write(msg+'\nMesh quality test failed\n')

    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    mycopyfile('test_mqual.cfg',wdir+'/Req_%s.%d/test_mqual.cfg'%(tag,cnt))
    
    return

def valid_anout(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    potind=get_potind(outfile)
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if E4D runs'%(tag,cnt)
    print('')
    print_splitter('Test Forward Simulation Mode (Analytic)','=',80)
    print(msg)
    
    if os.path.isfile('e4d.log'):
        print('Success: e4d.log was found')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
        return
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if %s exists'%(tag,cnt,sigsrv)
    print('')
    print_splitter('Test Forward Simulation Mode (Analytic)','=',80)
    print(msg)
    
    if os.path.isfile(sigsrv):
        print('Success: %s was found'%sigsrv)
    else:
        print('Failed: Forward modeling was not ran successfully')
        sys.stderr.write(msg+'\nForward modeling failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(outfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile))
    mycopyfile(sigsrv,wdir+'/Req_%s.%d/%s'%(tag,cnt,sigsrv))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if %s exists'%(tag,cnt,dpdfile)
    print('')
    print_splitter('Test Forward Simulation Mode (Analytic)','=',80)
    print(msg)
        
    if os.path.isfile(dpdfile):
        print('Success: %s was found'%dpdfile)
    else:
        print('Failed: Forward modeling was not ran successfully')
        sys.stderr.write(msg+'\nForward modeling failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(outfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile))
    mycopyfile(dpdfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,dpdfile))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if an_potential.* exists'%(tag,cnt)
    print('')
    print_splitter('Test Forward Simulation Mode (Analytic)','=',80)
    print(msg)
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    for ipot in potind:
        if os.path.isfile('an_potential.%d'%ipot):
            print('Success: an_potential.%d was found'%ipot)
        else:
            print('Failed: Forward modeling was not ran successfully')
            sys.stderr.write(msg+'\nForward modeling failed\n')
        mycopyfile('an_potential.%d'%ipot,wdir+'/Req_%s.%d/an_potential.%d'%(tag,cnt,ipot))

    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(outfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile))
    
    return

def valid_ansol(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    potind=get_potind(outfile)
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if all the forward modeling output files exist'%(tag,cnt)
    print('')
    print_splitter('Test Forward Simulation Mode (Analytic)','=',80)
    print(msg)
    
    if os.path.isfile(sigsrv):
        print('Success: %s was found'%sigsrv)
    else:
        print('Failed: Forward modeling output files were not found')
        sys.stderr.write(msg+'\nAnalytic solution test failed\n')
        return
        
    if os.path.isfile(dpdfile):
        print('Success: %s was found'%dpdfile)
    else:
        print('Failed: Forward modeling output files were not found')
        sys.stderr.write(msg+'\nAnalytic solution test failed\n')
        return
        
    for ipot in potind:
        if os.path.isfile('an_potential.%d'%ipot):
            print('Success: an_potential.%d was found'%ipot)
        else:
            print('Failed: Forward modeling output files were not found')
            sys.stderr.write(msg+'\nAnalytic solution test failed\n')
            return
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check simulated data against theoretical values'%(tag,cnt)
    print('')
    print_splitter('Test Forward Simulation Mode (Analytic)','=',80)
    print(msg)
    
    sigma=get_sigma(sigfile)
    nodes=get_nodes(nodefile,trnfile)
    epos,ecfg=get_survey(sigsrv)
    
    cond=np.mean(sigma)
    mask=nodes[:,-1]==1
    elev=np.mean(nodes[mask,2])
    mask=epos[:,-1]==1
    if elev<np.max(epos[mask,2]):
        elev=np.max(epos[mask,2])
    else:
        epos[mask,2]=elev
    
    if True:
        dpbulk=get_dpred(dpdfile)
        an_dpred=dpbulk[:,-1]
    else:
        an_dpred=ecfg[:,4]
    
    an_dpred2=np.zeros_like(an_dpred)
    for i in range(len(an_dpred2)):
        aind=ecfg[i,0].astype(int)-1
        bind=ecfg[i,1].astype(int)-1
        mind=ecfg[i,2].astype(int)-1
        nind=ecfg[i,3].astype(int)-1
        gfam=get_gf(epos[aind,0:4],epos[mind,0:4],elev)
        gfan=get_gf(epos[aind,0:4],epos[nind,0:4],elev)
        gfbm=get_gf(epos[bind,0:4],epos[mind,0:4],elev)
        gfbn=get_gf(epos[bind,0:4],epos[nind,0:4],elev)
        an_dpred2[i]=(gfam-gfan-gfbm+gfbn)/4/np.pi/cond
    
    error=np.max(abs(an_dpred-an_dpred2)/np.maximum(abs(an_dpred),abs(an_dpred2)))
    if error<5e-2:
        print('Success: Max rel_error of %s was %.6f'%(dpdfile,error))
    else:
        print('Failed: Max rel_error of %s was %.6f'%(dpdfile,error))
        sys.stderr.write(msg+'\nForward modeling failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(outfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile))
    mycopyfile(sigsrv,wdir+'/Req_%s.%d/%s'%(tag,cnt,sigsrv))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check simulated potentials against theoretical values'%(tag,cnt)
    print('')
    print_splitter('Test Forward Simulation Mode (Analytic)','=',80)
    print(msg)
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    for ipot in potind:
        an_pot=get_sigma('an_potential.'+str(ipot))
        aind=ecfg[ipot-1,0].astype(int)-1
        bind=ecfg[ipot-1,1].astype(int)-1
        gfa=get_gf(epos[aind,0:4],nodes[:,0:4],elev,rshift=True)
        gfb=get_gf(epos[bind,0:4],nodes[:,0:4],elev,rshift=True)
        an_pot2=(gfa-gfb)/4/np.pi/cond
        
        ra2=(epos[aind,0]-nodes[:,0])**2+(epos[aind,1]-nodes[:,1])**2+(epos[aind,2]-nodes[:,2])**2
        rb2=(epos[bind,0]-nodes[:,0])**2+(epos[bind,1]-nodes[:,1])**2+(epos[bind,2]-nodes[:,2])**2
        ia=np.argmin(ra2)
        ib=np.argmin(rb2)
        an_pot[ia],an_pot2[ia]=0,0
        an_pot[ib],an_pot2[ib]=0,0
        
        error=np.max(abs(an_pot-an_pot2)/(np.maximum(abs(an_pot),abs(an_pot2))+1e-15))
        if error<5e-2:
            print('Success: Max rel_error of an_potential.%d was %.6f'%(ipot,error))
        else:
            print('Failed: Max rel_error of an_potential.%d was %.6f'%(ipot,error))
            sys.stderr.write(msg+'\nForward modeling failed\n')
        mycopyfile('an_potential.%d'%ipot,wdir+'/Req_%s.%d/an_potential.%d'%(tag,cnt,ipot))
    
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(outfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile))
    
    return

def valid_numout_fmm(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    potind=get_potind(outfile_fmm)
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if E4D runs'%(tag,cnt)
    print('')
    print_splitter('Test Forward Simulation Mode','=',80)
    print(msg)
    
    if os.path.isfile('fmm.log'):
        print('Success: fmm.log was found')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
        return
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if %s exists'%(tag,cnt,sigsrv_fmm)
    print('')
    print_splitter('Test Forward Simulation Mode','=',80)
    print(msg)
    
    if os.path.isfile(sigsrv_fmm):
        print('Success: %s was found'%sigsrv_fmm)
    else:
        print('Failed: Forward modeling was not ran successfully')
        sys.stderr.write(msg+'\nForward modeling failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('fmm.inp',wdir+'/Req_%s.%d/fmm.inp'%(tag,cnt))
    mycopyfile('fmm.log',wdir+'/Req_%s.%d/fmm.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(outfile_fmm,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile_fmm))
    mycopyfile(sigsrv_fmm,wdir+'/Req_%s.%d/%s'%(tag,cnt,sigsrv_fmm))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if %s exists'%(tag,cnt,dpdfile_fmm)
    print('')
    print_splitter('Test Forward Simulation Mode','=',80)
    print(msg)
    
    if os.path.isfile(dpdfile_fmm):
        print('Success: %s was found'%dpdfile_fmm)
    else:
        print('Failed: Forward modeling was not ran successfully')
        sys.stderr.write(msg+'\nForward modeling failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('fmm.inp',wdir+'/Req_%s.%d/fmm.inp'%(tag,cnt))
    mycopyfile('fmm.log',wdir+'/Req_%s.%d/fmm.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(outfile_fmm,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile_fmm))
    mycopyfile(dpdfile_fmm,wdir+'/Req_%s.%d/%s'%(tag,cnt,dpdfile_fmm))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if potential.* exists'%(tag,cnt)
    print('')
    print_splitter('Test Forward Simulation Mode','=',80)
    print(msg)
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    for ipot in potind:
        if os.path.isfile('traveltime.%d'%ipot):
            print('Success: traveltime.%d was found'%ipot)
        else:
            print('Failed: Forward modeling was not ran successfully')
            sys.stderr.write(msg+'\nForward modeling failed\n')
        mycopyfile('traveltime.%d'%ipot,wdir+'/Req_%s.%d/potential.%d'%(tag,cnt,ipot))
    
    mycopyfile('fmm.inp',wdir+'/Req_%s.%d/fmm.inp'%(tag,cnt))
    mycopyfile('fmm.log',wdir+'/Req_%s.%d/fmm.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(outfile_fmm,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile_fmm))
    
    return

def valid_numout(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    potind=get_potind(outfile)
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if E4D runs'%(tag,cnt)
    print('')
    print_splitter('Test Forward Simulation Mode','=',80)
    print(msg)
    
    if os.path.isfile('e4d.log'):
        print('Success: e4d.log was found')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
        return
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if %s exists'%(tag,cnt,sigsrv)
    print('')
    print_splitter('Test Forward Simulation Mode','=',80)
    print(msg)
    
    if os.path.isfile(sigsrv):
        print('Success: %s was found'%sigsrv)
    else:
        print('Failed: Forward modeling was not ran successfully')
        sys.stderr.write(msg+'\nForward modeling failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(outfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile))
    mycopyfile(sigsrv,wdir+'/Req_%s.%d/%s'%(tag,cnt,sigsrv))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if %s exists'%(tag,cnt,dpdfile)
    print('')
    print_splitter('Test Forward Simulation Mode','=',80)
    print(msg)
    
    if os.path.isfile(dpdfile):
        print('Success: %s was found'%dpdfile)
    else:
        print('Failed: Forward modeling was not ran successfully')
        sys.stderr.write(msg+'\nForward modeling failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(outfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile))
    mycopyfile(dpdfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,dpdfile))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if potential.* exists'%(tag,cnt)
    print('')
    print_splitter('Test Forward Simulation Mode','=',80)
    print(msg)
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    for ipot in potind:
        if os.path.isfile('potential.%d'%ipot):
            print('Success: potential.%d was found'%ipot)
        else:
            print('Failed: Forward modeling was not ran successfully')
            sys.stderr.write(msg+'\nForward modeling failed\n')
        mycopyfile('potential.%d'%ipot,wdir+'/Req_%s.%d/potential.%d'%(tag,cnt,ipot))
    
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(outfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile))
    
    return

def valid_numsol(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    potind=get_potind(outfile)
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if all the forward modeling output files exist'%(tag,cnt)
    print('')
    print_splitter('Test Forward Simulation Mode','=',80)
    print(msg)
    
    if os.path.isfile(sigsrv):
        print('Success: %s was found'%sigsrv)
    else:
        print('Failed: Forward modeling output files were not found')
        sys.stderr.write(msg+'\nNumberical solution test failed\n')
        return
    
    if os.path.isfile(dpdfile):
        print('Success: %s was found'%dpdfile)
    else:
        print('Failed: Forward modeling output files were not found')
        sys.stderr.write(msg+'\nNumerical solution test failed\n')
        return
    
    for ipot in potind:
        if os.path.isfile('potential.%d'%ipot):
            print('Success: potential.%d was found'%ipot)
        else:
            print('Failed: Forward modeling output files were not found')
            sys.stderr.write(msg+'\nNumerical solution test failed\n')
            return
    
    for ipot in potind:
        if os.path.isfile('an_potential.%d'%ipot):
            print('Success: an_potential.%d was found'%ipot)
        else:
            print('Failed: Forward modeling ouput files were not found')
            sys.stderr.write(msg+'\nNumerical solution test failed\n')
            return
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check simulated data against analytic solutions'%(tag,cnt)
    print('')
    print_splitter('Test Forward Simulation Mode','=',80)
    print(msg)

    nodes=get_nodes(nodefile,trnfile)
    epos,ecfg=get_survey(srvfile)
    epos2,ecfg2=get_survey(sigsrv)
    
    if True:
        dpbulk=get_dpred(dpdfile)
        error=np.mean(abs(dpbulk[:,4]-dpbulk[:,5])/np.maximum(abs(dpbulk[:,4]),abs(dpbulk[:,5])))
    else:
        error=np.mean(abs(ecfg[:,4]-ecfg2[:,4])/np.maximum(abs(ecfg[:,4]),abs(ecfg2[:,4])))
    
    if error<0.05:
        print('Success: Mean rel_err of %s was %.6f'%(dpdfile,error))
    else:
        print('Error: Mean rel_err of %s was %.6f'%(dpdfile,error))
        sys.stderr.write(msg+'\nForward modeling failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(sigfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,sigfile))
    mycopyfile(dpdfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,dpdfile))
    mycopyfile(sigsrv,wdir+'/Req_%s.%d/%s'%(tag,cnt,sigsrv))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check simulated potentials against analytic solutions'%(tag,cnt)
    print('')
    print_splitter('Test Forward Simulation Mode','=',80)
    print(msg)

    for ipot in potind:
        an_pot=get_sigma('an_potential.'+str(ipot))
        an_pot2=get_sigma('potential.'+str(ipot))
        aind=ecfg[ipot-1,0].astype(int)-1
        bind=ecfg[ipot-1,1].astype(int)-1
        ra2=(epos[aind,0]-nodes[:,0])**2+(epos[aind,1]-nodes[:,1])**2+(epos[aind,2]-nodes[:,2])**2
        rb2=(epos[bind,0]-nodes[:,0])**2+(epos[bind,1]-nodes[:,1])**2+(epos[bind,2]-nodes[:,2])**2
        ia=np.argmin(ra2)
        ib=np.argmin(rb2)
        an_pot[ia],an_pot2[ia]=0,0
        an_pot[ib],an_pot2[ib]=0,0

        error=np.mean(abs(an_pot-an_pot2)/(np.maximum(abs(an_pot),abs(an_pot2))+1e-15))
        if error<0.05:
            print('Success: Mean rel_err of potential.%d was %.6f'%(ipot,error))
        else:
            print('Failed: Mean rel_err of potential.%d was %.6f'%(ipot,error))
            sys.stderr.write(msg+'\nForward modeling failed\n')
        
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(sigfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,sigfile))
    mycopyfile(sigsrv,wdir+'/Req_%s.%d/%s'%(tag,cnt,sigsrv))
    for ipot in potind:
        mycopyfile('potential.%d'%ipot,wdir+'/Req_%s.%d/potential.%d'%(tag,cnt,ipot))
    
    return

def valid_invout_fmm(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
        
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if E4D runs'%(tag,cnt)
    print('')
    print_splitter('Test Inversion Mode','=',80)
    print(msg)
    
    if os.path.isfile('fmm.log'):
        print('Success: fmm.log was found')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
        return
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if speed.* exists'%(tag,cnt)
    print('')
    print_splitter('Test Inversion Mode','=',80)
    print(msg)
    
    nsigma=0
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    while 1:
        nsigma=nsigma+1
        if not os.path.isfile('speed.%d'%nsigma):
            break
        else:
            mycopyfile('speed.%d'%nsigma,wdir+'/Req_%s.%d/speed.%d'%(tag,cnt,nsigma))
    if len(range(nsigma))>3:
        print('Success: Slowness files speed.1 to speed.%d were found'%(nsigma-1))
    else:
        print('Failed: Inversion was not ran successfully')
        sys.stderr.write(msg+'\nInversion failed\n')
    
    #mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    #for i in range(nsigma):
    #    mycopyfile('sigma.%d'%i,wdir+'/Req_%s.%d/sigma.%d'%(tag,cnt,i))
    mycopyfile('fmm.inp',wdir+'/Req_%s.%d/fmm.inp'%(tag,cnt))
    mycopyfile('fmm.log',wdir+'/Req_%s.%d/fmm.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(invfile_fmm,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile_fmm))
    mycopyfile(outfile_fmm,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile_fmm))
        
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if %s exists'%(tag,cnt,dpdfile_fmm)
    print('')
    print_splitter('Test Inversion Mode','=',80)
    print(msg)
    
    if os.path.isfile(dpdfile_fmm):
        print('Success: %s was found'%dpdfile_fmm)
    else:
        print('Failed: Inversion was not ran successfully')
        sys.stderr.write(msg+'\nInversion failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('fmm.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('fmm.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(invfile_fmm,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile_fmm))
    mycopyfile(outfile_fmm,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile_fmm))
    mycopyfile(dpdfile_fmm,wdir+'/Req_%s.%d/%s'%(tag,cnt,dpdfile_fmm))
    
    #Consider generate a visit picture of the inverison results
    return

def valid_invout(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
        
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if E4D runs'%(tag,cnt)
    print('')
    print_splitter('Test Inversion Mode','=',80)
    print(msg)
    
    if os.path.isfile('e4d.log'):
        print('Success: e4d.log was found')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
        return
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if sigma.* exists'%(tag,cnt)
    print('')
    print_splitter('Test Inversion Mode','=',80)
    print(msg)
    
    nsigma=0
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    while 1:
        nsigma=nsigma+1
        if not os.path.isfile('sigma.%d'%nsigma):
            break
        else:
            mycopyfile('sigma.%d'%nsigma,wdir+'/Req_%s.%d/sigma.%d'%(tag,cnt,nsigma))
    if len(range(nsigma))>3:
        print('Success: Conductivity files sigma.1 to sigma.%d were found'%(nsigma-1))
    else:
        print('Failed: Inversion was not ran successfully')
        sys.stderr.write(msg+'\nInversion failed\n')
    
    #mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    #for i in range(nsigma):
    #    mycopyfile('sigma.%d'%i,wdir+'/Req_%s.%d/sigma.%d'%(tag,cnt,i))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mycopyfile(outfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile))
        
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if %s exists'%(tag,cnt,dpdfile)
    print('')
    print_splitter('Test Inversion Mode','=',80)
    print(msg)
    
    if os.path.isfile(dpdfile):
        print('Success: %s was found'%dpdfile)
    else:
        print('Failed: Inversion was not ran successfully')
        sys.stderr.write(msg+'\nInversion failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mycopyfile(outfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile))
    mycopyfile(dpdfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,dpdfile))
    
    #Consider generate a visit picture of the inverison results
    return

def valid_misfit_fmm(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if fmm.log exists'%(tag,cnt)
    print('')
    print_splitter('Test Inversion Mode','=',80)
    print(msg)
    
    if os.path.isfile('fmm.log'):
        print('Success: fmm.log was found')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nInversion convergence test failed\n')
        return
        
    #====================================================================================================        
    beta_init=600
    min_red=0.05
    beta_red=0.5
    chi_targ=1.0
    
    chi2=[]
    speed=[]
    beta=[]
    #Logic disorder, correct below
    with open('fmm.log','r') as f:
        for line in f.readlines():
            if 'Chi2 is currently' in line:
                chi2.append(float(line.split()[3]))
            elif 'Decrease in objective function' in line:
                if 'sufficient' in line:
                    beta.append(float(line.split()[11]))
                else:
                    speed.append(float(line.split()[5]))
            elif 'Decreasing beta' in line:
                beta.append(float(line.split()[-1]))
            elif 'ADJUSTING' in line:
                break
    
    cnt=cnt+1
    msg='Requirement %s.%d: Check if inversion solution converges'%(tag,cnt)
    print('')
    print_splitter('Test Inversion Mode','=',80)
    print(msg)
    
    if chi2[-1]<=chi_targ:
        print('Success: Chi-squared was no greater than the target value')
    else:
        print('Failed: Chi2-squared was greater than the target value')
        sys.stderr.write(msg+'\nInversion failed\n')
        
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('fmm.inp',wdir+'/Req_%s.%d/fmm.inp'%(tag,cnt))
    mycopyfile('fmm.log',wdir+'/Req_%s.%d/fmm.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(invfile_fmm,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile_fmm))
    
    return

def valid_misfit(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if e4d.log exists'%(tag,cnt)
    print('')
    print_splitter('Test Inversion Mode','=',80)
    print(msg)
    
    if os.path.isfile('e4d.log'):
        print('Success: e4d.log was found')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nInversion convergence test failed\n')
        return
        
    #====================================================================================================        
    beta_init=100
    min_red=0.25
    beta_red=0.5
    chi_targ=1.0
    
    chi2=[]
    speed=[]
    beta=[]
    #Logic disorder, correct below
    with open('e4d.log','r') as f:
        for line in f.readlines():
            if 'Chi2 is currently' in line:
                chi2.append(float(line.split()[3]))
            elif 'Decrease in objective function' in line:
                if 'sufficient' in line:
                    beta.append(float(line.split()[11]))
                else:
                    speed.append(float(line.split()[5]))
            elif 'Decreasing beta' in line:
                beta.append(float(line.split()[-1]))
            elif 'ADJUSTING' in line:
                break
    
    cnt=cnt+1
    msg='Requirement %s.%d: Check if inversion solution converges'%(tag,cnt)
    print('')
    print_splitter('Test Inversion Mode','=',80)
    print(msg)

    if chi2[-1]<=chi_targ:
        print('Success: Chi-squared was no greater than the target value')
    else:
        print('Failed: Chi2-squared was greater than the target value')
        sys.stderr.write(msg+'\nInversion failed\n')
        
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))

    return

def valid_iminodes(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if the mesh configuration and node files exist'%(tag,cnt)
    print('')
    print_splitter('Test Mesh Generation Mode (IMI)','=',80)
    print(msg)

    if os.path.isfile(cfgfile):
        print('Success: %s was found'%cfgfile)
    else:
        print('Failed: Cannot find %s'%cfgfile)
        sys.stderr.write(msg+'\nMesh generation (IMI) failed\n')
        return
    
    if os.path.isfile(nodefile):
        print('Success: %s was found'%nodefile)
    else:
        print('Failed: Cannot find %s'%nodefile)
        sys.stderr.write(msg+'\nMesh generation (IMI) failed\n')
        return

    if os.path.isfile(trnfile):
        print('Success: %s was found'%trnfile)
    else:
        print('Failed: Cannot find %s'%trnfile)
        sys.stderr.write(msg+'\nMesh generation (IMI) failed\n')
        return

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check control points with negative flags in %s'%(tag,cnt,nodefile)
    print('')
    print_splitter('Test Mesh Generation Mode (IMI)','=',80)
    print(msg)
    
    get_mshcfg(cfgfile)
    nodes=get_nodes(nodefile,trnfile)
    for flag in np.unique(cpts[:,-1]):
        if flag>=0:
            continue
        mask=cpts[:,-1]==flag
        subcpts=cpts[mask,:]
        mask=nodes[:,-1]==flag
        subnodes=nodes[mask,:]
        if all(isclose(subcpts[:,1:4],subnodes[:len(subcpts),0:3])):
            print('Success: Control points with negative flag %d in %s and %s matched'%(flag,cfgfile,nodefile))
        else:
            print('Failed: Controll points with negative flag %d in %s and %s did not match'%(flag,cfgfile,nodefile))
            sys.stderr.write(msg+'\nMesh generation (IMI) failed\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(cfgfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,cfgfile))
    mycopyfile(nodefile,wdir+'/Req_%s.%d/%s'%(tag,cnt,nodefile))
    mycopyfile(trnfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,trnfile))
    
    return

def valid_sipsig(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if %s generated by e4d exists'%(tag,cnt,sigfile)
    print('')
    print_splitter('Test Mesh Generation Mode (SIP)','=',80)
    print(msg)
    
    if os.path.isfile(sigfile):
        print('Sucess: %s was found'%sigfile)
    else:
        print('Failed: Mesh was not generated successfully')
        sys.stderr.write(msg+'\nMesh generation failed\n')
        return
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if %s contains both real and imaginary parts'%(tag,cnt,sigfile)
    print('')
    print_splitter('Test Mesh Generation Mode (SIP)','=',80)
    print(msg)
    
    passed=True
    with open(sigfile) as f:
        f.readline()
        if len(f.readline().split())<2:
            passed=False
    
    if passed:
        print('Sucess: %s contains both real and imaginary parts'%sigfile)
    else:
        print('Failed: %s missing imaginary part in %s'%sigfile)
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(sigfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,sigfile))
    
    return

def valid_sipdpd(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if %s generated by e4d exists'%(tag,cnt,dpdfile)
    print('')
    print_splitter('Test Forward Simulation Mode (SIP)','=',80)
    print(msg)
    
    if os.path.isfile(dpdfile):
        print('Success: %s was found'%dpdfile)
    else:
        print('Failed: Mesh was not generated successfully')
        sys.stderr.write(msg+'\nForward simulation failed\n')
        return
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if %s contains both real and imaginary parts'%(tag,cnt,dpdfile)
    print('')
    print_splitter('Test Forward Simulation Mode (SIP)','=',80)
    print(msg)
    
    passed=True
    with open(dpdfile) as f:
        f.readline()
        if len(f.readline().split())<9:
            passed=False
    
    if passed:
        print('Success: %s contains both real and imaginary parts'%dpdfile)
    else:
        print('Failed: %s missing imaginary part in %s'%dpdfile)
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mycopyfile(dpdfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,dpdfile))
    
    return

def valid_modes(tag):
    #cnt=-1
    #wdir=os.path.join(root,'Req_'+tag)
    #myrmtree(wdir)
    #mymkdir(wdir)
    
    #====================================================================================================
    #cnt=cnt+1
    #msg='Requirement %s (a): Check if e4d input and log files exist'%(tag)
    #print('')
    #print_splitter('Test E4D Mode Keywords','=',80)
    #print(msg)
    
    #if os.path.isfile('e4d.inp') and os.path.isfile('e4d_old.inp'):
    #    print('Success: e4d.inp was found')
    #else:
    #    print('Failed: Cannot find e4d.inp')
    #    sys.stderr.write(msg+'\nE4D test for mode keywords failed\n')
    #    return

    #if os.path.isfile('e4d.log') and os.path.isfile('e4d_old.log'):
    #    print('Success: e4d.log was found')
    #else:
    #    print('Failed: Cannot find e4d.log')
    #    sys.stderr.write(msg+'\nE4D test for mode keywords failed\n')
    #    return        
    
    #====================================================================================================
    #cnt=cnt+1
    msg='Requirement %s: Check if the old and new mode keywords match'%(tag)
    print('')
    #print_splitter('Test E4D Mode Keywords','=',80)
    print(msg)
    
    if  not os.path.isfile('e4d.inp') or not os.path.isfile('e4d_old.inp'):
        print('Failed: Cannot find e4d.inp')
        sys.stderr.write(msg+'\nE4D test for mode keywords failed\n')
        return

    if not os.path.isfile('e4d.log') or not os.path.isfile('e4d_old.log'):
        print('Failed: Cannot find e4d.inp')
        sys.stderr.write(msg+'\nE4D test for mode keywords failed\n')
        return
    
    with open('e4d_old.inp') as f:
        mode=f.readline().split()[0]
    
    if mode=='1':
        key='ERT1'
    elif mode=='2':
        key='ERT2'
    elif mode=='3':
        key='ERT3'
    elif mode=='4':
        key='ERT4'
    elif mode=='5':
        key='ERT5'
    elif mode=='21':
        key='SIP1'
    elif mode=='22':
        key='SIP2'
    elif mode=='23':
        key='SIP3'
    elif mode=='24':
        key='SIP4'
    elif mode=='31':
        key='ERTtank1'
    elif mode=='32':
        key='ERTtank2'
    elif mode=='33':
        key='ERTtank3'
    elif mode=='34':
        key='ERTtank4'
    elif mode=='35':
        key='ERTtank5'
    elif mode=='41':
        key='SIPtank1'
    elif mode=='42':
        key='SIPtank2'
    elif mode=='43':
        key='SIPtank3'
    elif mode=='44':
        key='SIPtank4'
    elif mode=='\'analytic\'':
        key='ERTAnalytic'
    else:
        key=[]
    
    with open('e4d.log') as f:
        if key=='ERTAnalytic':
            for line in f.readlines():
                if 'RUNNING IN' in line:
                    if 'ANALYTIC' in line:
                        print('Success: E4D passed test')
                    else:
                        print('Failed: E4D did not pass test')
                        sys.stderr.write(msg+'\nE4D old and new mode keywords did not match\n')
                    break
        else:
            for line in f.readlines():
                if len(line.split())>0 and line.split()[0]=='Mode:':
                    if int(line.split()[1])==int(mode):
                        print('Success: E4D passed test')
                    else:
                        print('Failed: E4D did not pass test')
                        sys.stderr.write(msg+'\nE4D old and new mode keywords did not match\n')
                    break
    
    return

def run_tutorials(modes):
    #====================================================================================================
    #Available tutorials
    
    #1. tutorial/mode_1/metal_box_sheet_line (mode_1; ERT_IMI-mesh; included)
    #2. tutorial/mode_1/two_blocks(mode_1; ERT-mesh; included)
    #3. tutorial/mode_2/metal_box_sheet_line (mode_2; ERT_IMI-forward; included)
    #4. tutorial/mode_2/two_blocks (mode_2; ERT-forward; included)
    #5. tutorial/mode_22/metal_box_sheet_line (mode_22; SIP_IMI-forward; included)
    #6. tutorial/mode_3/metal_box_sheet_line (mode_3; ERT_IMI-inversion; included)
    #7. tutorial/mode_3/two_blocks (mode_3; ERT-inversion; included)
    #8. tutorial/mode_31/tank (mode_31; ERT_Tank-mesh; included)
    #9. tutorial/mode_32/tank (mode_32; ERT_Tank-forward; included)
    #10. tutorial/mode_4/sinking_plume (mode_4: ERT_TL-inversion; dismiss)
    #11. tutorial/mode_41/tank
    #12. tutorial/mode_42/tank
    
    #13. tutorial_JupyterLab/Electrical Methods/Forward modeling/mode_ERT2/metal_box_sheet_line (mode 2; ERT_IMI-forward; dismiss)
    #14. tutorial_JupyterLab/Electrical Methods/Forward modeling/mode_ERT2/two_blocks (mode2; ERT-forward; dismiss)
    #15. tutorial_JupyterLab/Electrical Methods/Forward modeling/mode_ERTtank2 (mode32; ERT_Tank-forward; dismiss)
    #16. tutorial_JupyterLab/Electrical Methods/Forward modeling/mode_SIP2/metal_box_sheet_line (mode22; SIP_IMI-forward; dismiss)
    #17. tutorial_JupyterLab/Electrical Methods/Forward modeling/mode_SIP2/two_blocks (mode22; SIP-forward; included)
    #18. tutorial_JupyterLab/Electrical Methods/Forward modeling/mode_SIPtank2 (mode42; SIP_Tank-forward; TBD)
    #19. tutorialJupyterLab/Electrical Methods/Inverse modeling/mode_ERT3/metal_box_sheet_line (mode3; ERT_IMI_inversion; dismiss)
    #20. tutorialJupyterLab/Electrical Methods/Inverse modeling/mode_ERT3/two_blocks (mode3; ERT-inversion; dismiss)
    #21. tutorial_JupyterLab/Electrical Methods/Mesh generation/mode_ERT1/metal_box_sheet_line (mode 1; ERT_IMI-mesh; dismiss)
    #22. tutorial_JupyterLab/Electrical Methods/Mesh generation/mode_ERT1/two_blocks (mode 1; ERT-mesh; dismiss)
    #23. tutorial_JupyterLab/Electrical Methods/Mesh generation/mode_ERTtank1 (mode 31; ERT_Tank-mesh; dismiss)
    #24. tutorial_JupyterLab/Electrical Methods/Mesh generation/mode_SIP1/two_blocks (mode 21; SIP-mesh; included)
    #25. tutorial_JupyterLab/Electrical Methods/Mesh generation/mode_SIPtank1 (mode 41; SIP_Tank-mesh; TBD)
    #26. tutorialJupyterLab/Electrical Methods/Time-lapse inverse modeling/mode_ERT4/sinking_plume (mode 4; ERT_TL-inversion; included)
    #27. tutorialJupyterLab/Travel-time Tomography/mode_1_Mesh generation/GPR
    #28. tutorialJupyterLab/Travel-time Tomography/mode_2_Forward modeling/GPR
    
    if isinstance(modes,str):
        modes=[modes]
    
    #====================================================================================================
    if 'TetGen' in modes or 'all' in modes or 'mesh' in modes:
        print('')
        print_splitter('Validate TetGen Version','=',80)

        sdir=root+'/include/tetgen'
        wdir=root+'/Req_2.0_TetGen'
        myrmtree(wdir)
        mymkdir(wdir)
        mycopyfile(sdir+'/200EW_T.cfg',wdir+'/200EW_T.cfg')
        mycopyfile(sdir+'/200EW_T.1.ele',wdir+'/200EW_T.1.ele.standard')
        mycopyfile(sdir+'/diff.sh',wdir+'/diff.sh')

        #Update tetgen/triangle/bx path
        print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('200EW_T')
        replace_line(cfgfile,'\'tetgen\'','\"'+tetgen+'\"')
        replace_line(cfgfile,'\'triangle\'','\"'+triangle+'\"')
        replace_line(cfgfile,'\'px\'','\''+bx+'\'')

        #Run mode 1
       # print('')
       # print('[Running mode %s] mpirun -np %d e4d'%('1',1))

        with open('e4d.inp','w') as f:
            f.write('1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
       
        #Use the diff function in linux and pipe the results to a file
        #command = 'diff <(head -n -1 %s) <(head -n -1 %s.standard) > check.txt'%(elefile,elefile)
        process=subprocess.Popen('bash diff.sh',shell=True)
        process.wait()
        
        print('Requirement_0.1.0: Check mesh quality using installed tetgen version')
        with open('check.txt') as f:
            lines=f.readlines()

        if not lines:
            print('Success: TetGen version test passed')
        else:
            print('Failed: TetGen version test did not pass')

    if 'ERT1' in modes or 'all' in modes or 'mesh' in modes:
        #Copy tutorial/mode_1/two_blocks (mode 1; ERT-mesh)
        print('')
        print_splitter('Test file setup for run Mode ERT1','=',80)

        #print('')
        #print('tar -C . -xzvf codes/e4d_dev/tutorial/mode_1/two_blocks.tgz')
        sdir=root+'/tutorial/mode_1'
        process=subprocess.Popen(['tar','-C',sdir,'-xzvf',sdir+'/two_blocks.tgz'],stdout=subprocess.DEVNULL)
        process.wait()

        sdir=root+'/tutorial/mode_1/two_blocks'
        wdir=root+'/Req_2.0_ERT1'
        myrmtree(wdir)
        mycopytree(sdir,wdir)

        #Update tetgen/triangle/bx path
        print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('two_blocks')
        replace_line(cfgfile,'\"../../../bin/tetgen\"','\"'+tetgen+'\"')
        replace_line(cfgfile,'\"../../../bin/triangle\"','\"'+triangle+'\"')
        replace_line(cfgfile,'\'../../../bin/bx\'','\''+bx+'\'')

        #Run mode 1
       # print('')
        print('[Running mode %s] mpirun -np %d e4d'%('1',1))

        with open('e4d.inp','w') as f:
            f.write('1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode ERT1
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')

        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('ERT1',1))

        with open('e4d.inp','w') as f:
            f.write('ERT1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
        
        print('E4D files set up.')
        
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.1')
        
    #====================================================================================================
    if 'ERTAnalytic' in modes or 'all' in modes or 'forward' in modes:
        #Copy tutorial/mode_2/two_blocks (mode 2; ERT-forward)
        print('')
        print_splitter('Test file setup for Run Mode ERTAnalytic','=',80)

        sdir=root+'/tutorial/mode_2/two_blocks'
        wdir=root+'/Req_3.0_ERTAnalytic'
        myrmtree(wdir)
        mycopytree(sdir,wdir)

        #Update tetgen/triangle/bx path
        #print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('two_blocks')
        replace_line(cfgfile,'\"../../../bin/tetgen\"','\"'+tetgen+'\"')
        replace_line(cfgfile,'\"../../../bin/triangle\"','\"'+triangle+'\"')
        replace_line(cfgfile,'\'../../../bin/bx\'','\''+bx+'\'')
        replace_line(cfgfile,'2 -2.5 0.0 -2.5  0.01 0.2      2 xz_2 yz_2 zz_2 mz_vol_2 cond_2',
                    '2 -2.5 0.0 -2.5  0.01 0.002      2 xz_2 yz_2 zz_2 mz_vol_2 cond_2')
        replace_line(cfgfile,'3  2.5 0.0 -2.5  0.01 0.0002','3  2.5 0.0 -2.5  0.01 0.002')
        replace_line(cfgfile,'4  0.0 0.0 -20.0 1e12 0.0002','4  0.0 0.0 -20.0 1e12 0.002')

        #Generate mesh
        #print('')
        #print('[Running mode %s] mpirun -np %d e4d'%('1',1))

        with open('e4d.inp','w') as f:
            f.write('1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode 'analytic'
        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('\'analytic\'',nproc))

        with open('e4d.inp','w') as f:
            f.write('\'analytic\'\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
        
        potind=[1549,1649,1749,1849]
        with open(outfile,'w') as f:
            f.write('1\n')
            f.write(dpdfile+'\n')
            f.write('%d\n'%len(potind))
            for ipot in potind:
                f.write('%d\n'%ipot)
            f.write('0\n')
            f.write('\'ASCII\'')

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode ERTAnalytic
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')

        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('ERTAnalytic',nproc))

        with open('e4d.inp','w') as f:
            f.write('ERTAnalytic\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
        
        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
    
        print('E4D files set up.')
        
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.2')
        
    
    #====================================================================================================
    if 'ERT2' in modes or 'all' in modes or 'forward' in modes:
        #Copy tutorial/mode_2/two_blocks (mode 2; ERT-forward)
        print('')
        print_splitter('Test file setup for Run Mode ERT2','=',80)

        sdir=root+'/tutorial/mode_2/two_blocks'
        wdir=root+'/Req_3.0_ERT2'
        myrmtree(wdir)
        mycopytree(sdir,wdir)
        mycopyfile(root+'/Req_3.0_ERTAnalytic/two_blocks.sig.srv',wdir+'/two_blocks.srv')
        mycopyfile(root+'/Req_3.0_ERTAnalytic/an_potential.1549',wdir+'/an_potential.1549')
        mycopyfile(root+'/Req_3.0_ERTAnalytic/an_potential.1649',wdir+'/an_potential.1649')
        mycopyfile(root+'/Req_3.0_ERTAnalytic/an_potential.1749',wdir+'/an_potential.1749')
        mycopyfile(root+'/Req_3.0_ERTAnalytic/an_potential.1849',wdir+'/an_potential.1849')

        #Update tetgen/triangle/bx path
        #print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('two_blocks')
        replace_line(cfgfile,'\"../../../bin/tetgen\"','\"'+tetgen+'\"')
        replace_line(cfgfile,'\"../../../bin/triangle\"','\"'+triangle+'\"')
        replace_line(cfgfile,'\'../../../bin/bx\'','\''+bx+'\'')
        replace_line(cfgfile,'2 -2.5 0.0 -2.5  0.01 0.2      2 xz_2 yz_2 zz_2 mz_vol_2 cond_2',
                    '2 -2.5 0.0 -2.5  0.01 0.002      2 xz_2 yz_2 zz_2 mz_vol_2 cond_2')
        replace_line(cfgfile,'3  2.5 0.0 -2.5  0.01 0.0002','3  2.5 0.0 -2.5  0.01 0.002')
        replace_line(cfgfile,'4  0.0 0.0 -20.0 1e12 0.0002','4  0.0 0.0 -20.0 1e12 0.002')

        #Generate mesh
        #print('')
        #print('[Running mode %s] mpirun -np %d e4d'%('1',1))

        with open('e4d.inp','w') as f:
            f.write('1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode 2
        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('2',nproc))

        with open('e4d.inp','w') as f:
            f.write('2\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
        
        potind=[1549,1649,1749,1849]
        with open(outfile,'w') as f:
            f.write('1\n')
            f.write(dpdfile+'\n')
            f.write('%d\n'%len(potind))
            for ipot in potind:
                f.write('%d\n'%ipot)
            f.write('0\n')
            f.write('\'ASCII\'')

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode ERT2
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')

        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('ERT2',nproc))

        with open('e4d.inp','w') as f:
            f.write('ERT2\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
        
        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
    
        print('E4D files set up.')
        
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.3')
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
    
    #====================================================================================================
    if 'ERT3' in modes or 'all' in modes or 'inversion' in modes:
        #Copy tutorial/mode_3/two_blocks (mode 3; ERT-inversion)
        print('')
        print_splitter('Testing file setup for Run Mode ERT3','=',80)

        sdir=root+'/tutorial/mode_3/two_blocks'
        wdir=root+'/Req_4.0_ERT3'
        myrmtree(wdir)
        mycopytree(sdir,wdir)
        mycopyfile(wdir+'/two_blocks_inv.cfg',wdir+'/two_blocks.cfg')
        mycopyfile(wdir+'/two_blocks_1.inv',wdir+'/two_blocks.inv')

        #Update tetgen/triangle/bx path
        #print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('two_blocks')
        replace_line(cfgfile,'\"../../../bin/tetgen\"','\"'+tetgen+'\"')
        replace_line(cfgfile,'\"../../../bin/triangle\"','\"'+triangle+'\"')
        replace_line(cfgfile,'\'../../../bin/bx\'','\''+bx+'\'')

        #Generate mesh
        #print('')
        #print('[Running mode %s] mpirun -np %d e4d'%('1',1))

        with open('e4d.inp','w') as f:
            f.write('1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode 3
        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('3',nproc))

        with open('e4d.inp','w') as f:
            f.write('3\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write('\'average\'\n')
            f.write(outfile+'\n')
            f.write(invfile+'\n')
            f.write('none\n')
        
        with open(outfile,'w') as f:
            f.write('1\n')
            f.write('%s\n'%dpdfile)
            f.write('0\n')

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode ERT3
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')

        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('ERT3',nproc))

        with open('e4d.inp','w') as f:
            f.write('ERT3\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write('\'average\'\n')
            f.write(outfile+'\n')
            f.write(invfile+'\n')
            f.write('none\n')

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
        
        
        print('E4D files set up.')
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.4')    
    #====================================================================================================
    if 'ERT4' in modes or 'all' in modes or 'inversion' in modes:
        #Copy tutorial/mode_3/two_blocks (mode 3; ERT-inversion)
        print('')
        print_splitter('Run Mode ERT4','=',80)

        if False:
            sdir=root+'/tutorial/mode_4/sinking_plume'
            wdir=root+'/Req_4.0_ERT4'
            myrmtree(wdir)
            mycopytree(sdir,wdir)

            process=subprocess.Popen(['tar','-C',wdir,'-xzvf',wdir+'/sp.tgz','--strip-components=1'],stdout=subprocess.DEVNULL)
            process.wait()

            process=subprocess.Popen(['tar','-C',wdir,'-xzvf',wdir+'/surveys.tgz','--strip-components=1'],stdout=subprocess.DEVNULL)
            process.wait()
        else:
            sdir=root+'/tutorial_JupyterLab/Electrical Methods/Time-lapse inverse modeling/mode_ERT4/sinking_plume/inverse/time_lapse'
            wdir=root+'/Req_4.0_ERT4'
            myrmtree(wdir)
            mycopytree(sdir,wdir)
        
        #print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('sp')
        mymove('surveys.txt','surveys_org.txt')
        
        with open('surveys.txt','w') as f:
            f.write('3\n')
            f.write('sig_0.0.sig.srv        0.0\n')
            f.write('sig_5.0.sig.srv        5.0\n')
            f.write('sig_10.0.sig.srv      10.0\n')
        
        #Run mode 4
        mycopyfile('e4d.inp','e4d_org.inp')
        replace_line('e4d.inp','ERT4','4')
        
        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('4',nproc))
        
        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
        
        #Run mode ERT4
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')
        mymove('e4d_org.inp','e4d.inp')

        print('')
        print('[Running mode %s] mpirun -np %d e4d'%('ERT4',nproc))
        
        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
        
        print('E4D files set up.')
        
        valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.5')     
    #====================================================================================================
    if 'ERT1-IMI' in modes or 'all' in modes or 'mesh' in modes:
        #Copy tutorial/mode_1/metal_box_sheet_line (mode 1; ERT_IMI-mesh)
        print('')
        print_splitter('Set up files for Run Mode ERT1 (IMI)','=',80)

        #print('')
        #print('tar -C . -xzvf codes/e4d_dev/tutorial/mode_1/mbsl.tgz')
        sdir=root+'/tutorial/mode_1'
        process=subprocess.Popen(['tar','-C',sdir,'-xzvf',sdir+'/mbsl.tgz'],stdout=subprocess.DEVNULL)
        process.wait()

        sdir=root+'/tutorial/mode_1/metal_box_sheet_line'
        wdir=root+'/Req_2.0_ERT1-IMI'
        myrmtree(wdir)
        mycopytree(sdir,wdir)

        #Update tetgen/triangle/bx path
        #print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('mbsl')
        replace_line(cfgfile,'\"../../../bin/tetgen\"','\"'+tetgen+'\"')
        replace_line(cfgfile,'\"../../../bin/triangle\"','\"'+triangle+'\"')
        replace_line(cfgfile,'\'../../../bin/bx\'','\''+bx+'\'')

        #Run mode 1 (IMI)
        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('1 (IMI)',1))

        with open('e4d.inp','w') as f:
            f.write('1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode ERT1 (IMI)
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')

        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('ERT1 (IMI)',1))

        with open('e4d.inp','w') as f:
            f.write('ERT1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
    

        print('E4D files set up.')
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.6')    
    
    #====================================================================================================
    if 'ERT2-IMI' in modes or 'all' in modes or 'forward' in modes:
        #Copy tutorial/mode_2/metal_box_sheet_line (mode 2; ERT_IMI-forward)
        print('')
        print_splitter('Test file setup for Run Mode ERT2 (IMI)','=',80)

        sdir=root+'/tutorial/mode_2/metal_box_sheet_line'
        wdir=root+'/Req_3.0_ERT2-IMI'
        myrmtree(wdir)
        mycopytree(sdir,wdir)
        
        #Update tetgen/triangle/bx path
        #print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('mbsl')
        replace_line(cfgfile,'\"../../../bin/tetgen\"','\"'+tetgen+'\"')
        replace_line(cfgfile,'\"../../../bin/triangle\"','\"'+triangle+'\"')
        #replace_line(cfgfile,'\'../../../bin/bx\'','\''+bx+'\'')
        replace_line(cfgfile,'\'px\'','\''+bx+'\'')
        
        #Generate mesh
        #print('')
        #print('[Running mode %s] mpirun -np %d e4d'%('1',1))
        
        with open('e4d.inp','w') as f:
            f.write('1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode 2 (IMI)
        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('2 (IMI)',nproc))

        with open('e4d.inp','w') as f:
            f.write('2\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
        
        potind=[2071,2072]
        with open(outfile,'w') as f:
            f.write('1\n')
            f.write(dpdfile+'\n')
            f.write('%d\n'%len(potind))
            for ipot in potind:
                f.write('%d\n'%ipot)
            f.write('0\n')
            f.write('\'ASCII\'')

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode ERT2 (IMI)
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')

        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('ERT2 (IMI)',nproc))

        with open('e4d.inp','w') as f:
            f.write('ERT2\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
        
        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
    

        print('E4D files set up.')
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.7')    
        
    
    #====================================================================================================
    if 'ERT3-IMI' in modes or 'all' in modes or 'inversion' in modes:
        #Copy tutorial/mode_3/metal_box_sheet_line (mode 3; ERT_IMI-inversion)
        print('')
        print_splitter('Test file set up for Run Mode ERT3 (IMI)','=',80)

        sdir=root+'/tutorial/mode_3/metal_box_sheet_line'
        wdir=root+'/Req_4.0_ERT3-IMI'
        myrmtree(wdir)
        mycopytree(sdir,wdir)
        mycopyfile(wdir+'/mbsl_inv.cfg',wdir+'/mbsl.cfg')
        mycopyfile(wdir+'/mbsl_dipping_plane.srv',wdir+'/mbsl.srv')
        mycopyfile(wdir+'/mbsl_1.inv',wdir+'/mbsl.inv')

        #Update tetgen/triangle/bx path
        #print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('mbsl')
        replace_line(cfgfile,'\"../../../bin/tetgen\"','\"'+tetgen+'\"')
        replace_line(cfgfile,'\"../../../bin/triangle\"','\"'+triangle+'\"')
        replace_line(cfgfile,'\'../../../bin/bx\'','\''+bx+'\'')

        #Generate mesh
        #print('')
        #print('[Running mode %s] mpirun -np %d e4d'%('1',1))

        with open('e4d.inp','w') as f:
            f.write('1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode 3 (IMI)
        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('3 (IMI)',nproc))

        with open('e4d.inp','w') as f:
            f.write('3\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write('0.001\n')
            f.write(outfile+'\n')
            f.write(invfile+'\n')
            f.write('none\n')
            
        with open(outfile,'w') as f:
            f.write('1\n')
            f.write('%s\n'%dpdfile)
            f.write('0\n')

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode ERT3 (IMI)
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')

        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('ERT3 (IMI)',nproc))

        with open('e4d.inp','w') as f:
            f.write('ERT3\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write('0.001\n')
            f.write(outfile+'\n')
            f.write(invfile+'\n')
            f.write('none\n')

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
    
        print('E4D files set up.')
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.8')     
    #====================================================================================================
    if 'SIP1' in modes or 'all' in modes or 'mesh' in modes:
        #Copy tutorial_JupyterLab/Electrical Methods/Mesh generation/mode_SIP1/two_blocks (mode 21; SIP-mesh)
        print('')
        print_splitter('Testing file setup for Run Mode SIP1','=',80)
        
        sdir=root+'/tutorial_JupyterLab/Electrical Methods/Mesh generation/mode_SIP1/two_blocks'
        wdir=root+'/Req_2.0_SIP1'
        myrmtree(wdir)
        mycopytree(sdir,wdir)

        #Update tetgen/triangle/bx path
        #print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('two_blocks')
        replace_line(cfgfile,'\"tetgen\"','\"'+tetgen+'\"')
        replace_line(cfgfile,'\"triangle\"','\"'+triangle+'\"')
        replace_line(cfgfile,'\'px\'','\''+bx+'\'')

        #Run mode 21
        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('21',1))

        with open('e4d.inp','w') as f:
            f.write('21\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode SIP
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')

        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('SIP1',1))

        with open('e4d.inp','w') as f:
            f.write('SIP1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
        
        print('E4D files set up.')
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.9') 
        
    #====================================================================================================
    if 'SIP2' in modes or 'all' in modes or 'forward' in modes:
        #Copy tutorial_JupyterLab/Electrical Methods/Forward modeling/mode_SIP2/two_blocks (mode22; SIP-forward)
        print('')
        print_splitter('Testing file setup for Run Mode SIP2','=',80)

        sdir=root+'/tutorial_JupyterLab/Electrical Methods/Forward modeling/mode_SIP2/two_blocks'
        wdir=root+'/Req_3.0_SIP2'
        myrmtree(wdir)
        mycopytree(sdir,wdir)
        
        #Update tetgen/triangle/bx path
        #print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('two_blocks')
        replace_line(cfgfile,'\"tetgen\"','\"'+tetgen+'\"')
        replace_line(cfgfile,'\"triangle\"','\"'+triangle+'\"')
        replace_line(cfgfile,'\'px\'','\''+bx+'\'')
        
        #Generate mesh
        #print('')
        #print('[Running mode %s] mpirun -np %d e4d'%('22',1))
        
        with open('e4d.inp','w') as f:
            f.write('21\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode 22
        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('22',nproc))

        with open('e4d.inp','w') as f:
            f.write('22\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
        
        potind=[1449]
        with open(outfile,'w') as f:
            f.write('1\n')
            f.write(dpdfile+'\n')
            f.write('%d\n'%len(potind))
            for ipot in potind:
                f.write('%d\n'%ipot)
            f.write('0\n')
            f.write('\'ASCII\'')

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode SIP2
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')

        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('SIP2',nproc))

        with open('e4d.inp','w') as f:
            f.write('SIP2\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
        
        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
    
        print('E4D files set up.')
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.10') 

    #====================================================================================================
    if 'SIP3' in modes or 'all' in modes or 'inversion' in modes:
        print('')
        print_splitter('Run Mode SIP3','=',80)

        print('')
        print('Requirement 0.2.11: Tutorial for mode SIP3 is currently unavailable. Skipping')
    
    #====================================================================================================
    if 'SIP1-IMI' in modes or 'all' in modes or 'mesh' in modes:
        print('')
        print_splitter('Run Mode SIP1 (IMI)','=',80)

        print('')
        print('Requirement 0.2.12: Tutorial for mode SIP1 (IMI) is currently unavailable. Skipping')
    
    #====================================================================================================
    if 'SIP2-IMI' in modes or 'all' in modes or 'forward' in modes:
        #Copy tutorial/mode_22/metal_box_sheet_line (mode 22; SIP_IMI-forward)
        print('')
        print_splitter('Run Mode SIP2 (IMI)','=',80)

        sdir=root+'/tutorial/mode_22/metal_box_sheet_line'
        wdir=root+'/Req_3.0_SIP2-IMI'
        myrmtree(wdir)
        mycopytree(sdir,wdir)
        
        #Update tetgen/triangle/bx path
        print('')
        print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('mbsl')
        replace_line(cfgfile,'\"tetgen\"','\"'+tetgen+'\"') #bug fixed
        replace_line(cfgfile,'\"triangle\"','\"'+triangle+'\"') #bug fixed
        replace_line(cfgfile,'\'bx\'','\''+bx+'\'') #bug fixed
        
        #Generate mesh
        #print('')
        #print('[Running mode %s] mpirun -np %d e4d'%('21',1))
        
        with open('e4d.inp','w') as f:
            f.write('21\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode 22 (IMI)
        print('')
        print('[Running mode %s] mpirun -np %d e4d'%('22 (IMI)',nproc))

        with open('e4d.inp','w') as f:
            f.write('22\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
        
        potind=[1415]
        with open(outfile,'w') as f:
            f.write('1\n')
            f.write(dpdfile+'\n')
            f.write('%d\n'%len(potind))
            for ipot in potind:
                f.write('%d\n'%ipot)
            f.write('0\n')
            f.write('\'ASCII\'')

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode ERT2 (IMI)
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')

        print('')
        print('[Running mode %s] mpirun -np %d e4d'%('SIP2 (IMI)',nproc))

        with open('e4d.inp','w') as f:
            f.write('SIP2\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
        
        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
    
        print('E4D files set up.')
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.13') 

    #====================================================================================================
    if 'SIP3-IMI' in modes or 'all' in modes or 'inversion' in modes:
        print('')
        print_splitter('Run Mode SIP3 (IMI)','=',80)

        print('')
        print('Requirement 0.2.14: Tutorial for mode SIP3 (IMI) is currently unavailable. Skipping')
    
    #====================================================================================================
    if 'ERTtank1' in modes or 'all' in modes or 'mesh' in modes:
        #Copy tutorial/mode_31/tank (mode 31; ERT_Tank-mesh)
        print('')
        print_splitter('Run Mode ERTtank1','=',80)

        sdir=root+'/tutorial/mode_31/tank'
        wdir=root+'/Req_2.0_ERTtank1'
        myrmtree(wdir)
        mycopytree(sdir,wdir)

        #Update tetgen/triangle/bx path
        #print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('tank')
        replace_line(cfgfile,'\'tetgen\'','\"'+tetgen+'\"')
        replace_line(cfgfile,'\'triangle\'','\"'+triangle+'\"')
        replace_line(cfgfile,'\'bx\'','\''+bx+'\'')

        #Run mode 31
        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('31',1))

        with open('e4d.inp','w') as f:
            f.write('31\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode ERT1 (IMI)
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')

        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('ERTtank1',1))

        with open('e4d.inp','w') as f:
            f.write('ERTtank1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
    
        print('E4D files set up.')
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.15') 

    
    #====================================================================================================
    if 'ERTtank2' in modes or 'all' in modes or 'forward' in modes:
        #Copy tutorial/mode_32/tank (mode 32; ERT_Tank-forward)
        print('')
        print_splitter('Run Mode ERTtank2','=',80)

        sdir=root+'/tutorial/mode_32/tank'
        wdir=root+'/Req_3.0_ERTtank2'
        myrmtree(wdir)
        mycopytree(sdir,wdir)
        
        #Update tetgen/triangle/bx path
        #print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('tank')
        replace_line(cfgfile,'\'tetgen\'','\"'+tetgen+'\"')
        replace_line(cfgfile,'\'triangle\'','\"'+triangle+'\"')
        replace_line(cfgfile,'\'bx\'','\''+bx+'\'')
        
        #Generate mesh
        #print('')
        #print('[Running mode %s] mpirun -np %d e4d'%('31',1))
        
        with open('e4d.inp','w') as f:
            f.write('31\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode 32
       # print('')
        print('[Running mode %s] mpirun -np %d e4d'%('32',nproc))

        with open('e4d.inp','w') as f:
            f.write('32\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
        
        potind=[1,2,3,4,5,6]
        with open(outfile,'w') as f:
            f.write('1\n')
            f.write(dpdfile+'\n')
            f.write('%d\n'%len(potind))
            for ipot in potind:
                f.write('%d\n'%ipot)
            f.write('0\n')
            f.write('\'ASCII\'')

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode ERT2 (IMI)
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')

        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('ERTtank2',nproc))

        with open('e4d.inp','w') as f:
            f.write('ERTtank2\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
        
        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
    
        print('E4D files set up.')
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.16') 

    
    #====================================================================================================
    if 'ERTtank3' in modes or 'all' in modes or 'inversion' in modes:
        print('')
        print_splitter('Run Mode ERTtank3','=',80)

        print('')
        print('Requirement 0.2.17: Tutorial for mode ERTtank3 is currently unavailable. Skipping')
    
    #====================================================================================================
    if 'SIPtank1' in modes or 'all' in modes or 'mesh' in modes:
        #Copy tutorial/mode_41/tank (mode 41; SIP_Tank-mesh)
        print('')
        print_splitter('Run Mode SIPtank1','=',80)

        sdir=root+'/tutorial/mode_41/tank'
        wdir=root+'/Req_2.0_SIPtank1'
        myrmtree(wdir)
        mycopytree(sdir,wdir)

        #Update tetgen/triangle/bx path
        #print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('tank')
        replace_line(cfgfile,'\'tetgen\'','\"'+tetgen+'\"')
        replace_line(cfgfile,'\'triangle\'','\"'+triangle+'\"')
        replace_line(cfgfile,'\'bx\'','\''+bx+'\'')

        #Run mode 41
        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('41',1))

        with open('e4d.inp','w') as f:
            f.write('41\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode SIPtank1
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')

        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('SIPtank1',1))

        with open('e4d.inp','w') as f:
            f.write('SIPtank1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
        
        print('E4D files set up.')
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.18') 

        
    #====================================================================================================
    if 'SIPtank2' in modes or 'all' in modes or 'forward' in modes:
        #Copy tutorial/mode_42/tank (mode 42; SIP_Tank-forward)
        print('')
        print_splitter('Run Mode SIPtank2','=',80)

        sdir=root+'/tutorial/mode_42/tank'
        wdir=root+'/Req_3.0_SIPtank2'
        myremove(sdir+'/.#pots.txt')
        myrmtree(wdir)
        mycopytree(sdir,wdir)
        
        #Update tetgen/triangle/bx path
        #print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars('tank')
        replace_line(cfgfile,'\'tetgen\'','\"'+tetgen+'\"')
        replace_line(cfgfile,'\'triangle\'','\"'+triangle+'\"')
        replace_line(cfgfile,'\'bx\'','\''+bx+'\'')
        
        #Generate mesh
        #print('')
        #print('[Running mode %s] mpirun -np %d e4d'%('41',1))
        
        with open('e4d.inp','w') as f:
            f.write('41\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode 32
        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('42',nproc))

        with open('e4d.inp','w') as f:
            f.write('42\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
        
        potind=[1,2,3,4,5,6]
        with open(outfile,'w') as f:
            f.write('1\n')
            f.write(dpdfile+'\n')
            f.write('%d\n'%len(potind))
            for ipot in potind:
                f.write('%d\n'%ipot)
            f.write('0\n')
            f.write('\'ASCII\'')

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode SIPtank2
        mymove('e4d.inp','e4d_old.inp')
        mymove('e4d.log','e4d_old.log')
        mymove('run.log','run_old.log')

        #print('')
        print('[Running mode %s] mpirun -np %d e4d'%('SIPtank2',nproc))

        with open('e4d.inp','w') as f:
            f.write('SIPtank2\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
        
        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
    
        print('E4D files set up.')
        #valid_modes('_'.join(os.getcwd().split('/')[-1].split('_')[1:]))
        valid_modes('0.2.19') 

    
    #====================================================================================================
    if 'SIPtank3' in modes or 'all' in modes or 'inversion' in modes:
        print('')
        print_splitter('Run Mode SIPtank3','=',80)

        print('')
        print('Requirement 0.2.20: Tutorial for mode ERTtank3 is currently unavailable. Skipping')
        
    if 'FMM2' in modes or 'all' in modes or 'forward' in modes:
        #Copy extensions/mode_2/borehole (mode 2; FMM-forward)
        print('')
        print_splitter('Run Mode 2 (FMM)','=',80)

        sdir=root+'/include/mode_2/borehole'
        wdir=root+'/Req_3.0_FMM2'
        myrmtree(wdir)
        mycopytree(sdir,wdir)
        
        #Update tetgen/triangle/bx path
        #print('')
        #print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars_fmm('borehole')
        replace_line(cfgfile,'\"tetgen\"','\"'+tetgen+'\"')
        replace_line(cfgfile,'\"triangle\"','\"'+triangle+'\"')
        replace_line(cfgfile,'\'bx\'','\''+bx+'\'')
        
        #Generate mesh
        #print('')
        #print('[Running mode %s] mpirun -np %d e4d'%('1',1))
        
        with open('e4d.inp','w') as f:
            f.write('1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        #Run mode 2 (FMM)
        #print('')
        print('[Running mode %s] mpirun -np %d e4d -fmm %d'%('2 (FMM)',nproc,nproc))

        with open('fmm.inp','w') as f:
            f.write('2\n')
            f.write(nodefile+'\n')
            f.write(srvfile_fmm+'\n')
            f.write(sigfile_fmm+'\n')
            f.write(outfile_fmm+'\n')
        
        potind=[1,5]
        with open(outfile_fmm,'w') as f:
            f.write('1\n')
            f.write(dpdfile_fmm+'\n')
            f.write('%d\n'%len(potind))
            for ipot in potind:
                f.write('%d\n'%ipot)
            f.write('0\n')
            f.write('\'ASCII\'')
        
        mycopyfile('borehole.sig','borehole.vel')
        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d,'-fmm',str(nproc)],stdout=f)
            process.wait()
    
    if 'FMM3' in modes or 'all' in modes or 'inversion' in modes:
        #Copy extensions/mode_3/borehole (mode 3; FMM-inversion)
        print('')
        print_splitter('Run Mode 3 (FMM)','=',80)

        sdir=root+'/include/mode_3/borehole'
        wdir=root+'/Req_4.0_FMM3'
        myrmtree(wdir)
        mycopytree(sdir,wdir)
        mycopyfile(wdir+'/borehole_inv.cfg',wdir+'/borehole.cfg')
        mycopyfile(wdir+'/borehole_1.inv',wdir+'/borehole.inv')
        
        #Update tetgen/triangle/bx path
        print('')
        print('cd %s'%wdir)
        os.chdir(wdir)
        set_globvars_fmm('borehole')
        replace_line(cfgfile,'\"tetgen\"','\"'+tetgen+'\"')
        replace_line(cfgfile,'\"triangle\"','\"'+triangle+'\"')
        replace_line(cfgfile,'\'bx\'','\''+bx+'\'')

        #Generate mesh
        #print('')
        #print('[Running mode %s] mpirun -np %d e4d'%('1',1))

        with open('e4d.inp','w') as f:
            f.write('1\n')
            f.write('%s\n'%cfgfile)

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()
        
        #Run mode 3 (FMM)
        print('')
        print('[Running mode %s] mpirun -np %d e4d -fmm %d'%('3 (FMM)',nproc,nproc))
        
        with open('fmm.inp','w') as f:
            f.write('3\n')
            f.write(nodefile+'\n')
            f.write(srvfile_fmm+'\n')
            f.write('10\n')
            f.write(outfile_fmm+'\n')
            f.write(invfile_fmm+'\n')
            f.write('none\n')
            #f.write('none\n')
            
        with open(outfile_fmm,'w') as f:
            f.write('1\n')
            f.write('%s\n'%dpdfile_fmm)
            f.write('0\n')

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d,'-fmm',str(nproc)],stdout=f)
            process.wait()
        
    return

def valid_fmminp(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    sigfile_fmm='10'
    refsig_fmm='none'
    mycopyfile('fmm.inp','fmm_copy.inp')
    mycopyfile('fmm.log','fmm_copy.log')
    mycopyfile('run.log','run_copy.log')
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if the primary input file fmm.inp exists'%(tag,cnt)+\
    '\n... Cannot find the primary input file fmm.inp'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    myremove('fmm.inp')
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d,'-fmm',str(nproc)],stdout=f)
        process.wait()
    
    if os.path.isfile('fmm.log'):
        with open('fmm.log','r') as f:
            if 'Cannot find the primary input file fmm.inp' in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Invalid mode number in fmm.inp'%(tag,cnt)+\
    '\n... The mode selected in fmm.inp is   1, which is invalid'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('fmm.inp','w') as f:
        f.write('1\n')
        f.write('%s\n'%cfgfile)

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d,'-fmm',str(nproc)],stdout=f)
        process.wait()
    
    if os.path.isfile('fmm.log'):
        with open('fmm.log','r') as f:
            if 'The mode selected in fmm.inp is   1, which is invalid' in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')

    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('fmm.inp',wdir+'/Req_%s.%d/fmm.inp'%(tag,cnt))
    mymove('fmm.log',wdir+'/Req_%s.%d/fmm.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    mymove('fmm_copy.inp','fmm.inp')
    mymove('fmm_copy.log','fmm.log')
    mymove('run_copy.log','run.log')
    return

def valid_e4dinp(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    sigfile='\'average\''
    refsig='none'
    mycopyfile('e4d.inp','e4d_copy.inp')
    mycopyfile('e4d.log','e4d_copy.log')
    mycopyfile('run.log','run_copy.log')
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if the primary input file e4d.inp exists'%(tag,cnt)+\
    '\n... Cannot find the primary input file e4d.inp'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    myremove('e4d.inp')
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'Cannot find the primary input file e4d.inp' in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')

    #mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    #mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    #mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Missing the mode number in e4d.inp'%(tag,cnt)+\
    '\n... There was a problem reading the mode in e4d.inp'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'There was a problem reading the mode in e4d.inp' in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')

    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Missing the mesh file name in e4d.inp'%(tag,cnt)+\
    '\n... There was a problem reading the mesh file name in e4d.inp'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'There was a problem reading the mesh file name in e4d.inp' in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')

    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Missing the survey file name in e4d.inp'%(tag,cnt)+\
    '\n... There was a problem reading the survey file name in e4d.inp'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'There was a problem reading the survey file name in e4d.inp' in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Missing the conductivity file name in e4d.inp'%(tag,cnt)+\
    '\n... There was a problem reading the conductivity file name in e4d.inp'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'There was a problem reading the conductivity file name in e4d.inp' in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Missing the output options file name in e4d.inp'%(tag,cnt)+\
    '\n... There was a problem reading the output options file name in e4d.inp'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write('average.sig\n') #There is a bug with 'average', two_blocks.sig, etc.

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'There was a problem reading the output options file name in e4d.inp' in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Missing the inverse options file name in e4d.inp'%(tag,cnt)+\
    '\n... There was a problem reading the inverse options file name in e4d.inp'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'There was a problem reading the inverse options file name in e4d.inp' in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Missing the reference model file name in e4d.inp'%(tag,cnt)+\
    '\n... There was a problem reading the reference model file name in e4d.inp'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'There was a problem reading the reference model file name in e4d.inp' in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Missing the time-lapse survey list file name in e4d.inp'%(tag,cnt)+\
    '\n... There was a problem reading the time-lapse survey file name'+\
    '\n... and/or reference model update option in e4d.inp'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('4\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()

    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'There was a problem reading the time-lapse survey file name'+\
            ' and/or reference model update option in e4d.inp' in f.read().replace('\n',''):
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')

    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Missing the time-lapse reference model option in e4d.inp'%(tag,cnt)+\
    '\n... There was a problem reading the time-lapse survey file name'+\
    '\n... and/or reference model update option in e4d.inp'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('4\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
        f.write('surveys.txt\n')
    
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()

    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'There was a problem reading the time-lapse survey file name'+\
            ' and/or reference model update option in e4d.inp' in f.read().replace('\n',''):
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')

    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: An invalid mode number was input in e4d.inp'%(tag,cnt)+\
    '\n... The mode selected in e4d.inp is   6, which is invalid'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('6\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'The mode selected in e4d.inp is   6, which is invalid' in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: An invalid mode string was input in e4d.inp'%(tag,cnt)+\
    '\n... There was a problem reading the mode in e4d.inp'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('ERT6\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'There was a problem reading the mode in e4d.inp' in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    mymove('e4d_copy.inp','e4d.inp')
    mymove('e4d_copy.log','e4d.log')
    mymove('run_copy.log','run.log')
    return

def valid_cfgfile(tag):
    cnt=0
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    #nproc=1 #may be removed
    mycopyfile('e4d.inp','e4d_copy.inp')
    mycopyfile('e4d.log','e4d_copy.log')
    mycopyfile('run.log','run_copy.log')
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: A mesh configuration file that was not in the directory was input in e4d.inp'%(tag,cnt)+\
    '\n... Cannot find the mesh configuration file: %s'%cfgfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('1\n')
        f.write(cfgfile+'\n')
    
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'Cannot find the mesh configuration file: %s'%cfgfile in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
        
        mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    mymove('e4d_copy.inp','e4d.inp')
    mymove('e4d_copy.log','e4d.log')
    mymove('run_copy.log','run.log')
    return

def valid_mshfile_fmm(tag):
    cnt=0
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    sigfile_fmm='10'
    refsig_fmm='none'
    mycopyfile('fmm.inp','fmm_copy.inp')
    mycopyfile('fmm.log','fmm_copy.log')
    mycopyfile('run.log','run_copy.log')

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: A mesh node file that was not in the directory was input in fmm.inp'%(tag,cnt)+\
    '\n... Cannot find the specified mesh node file: %s'%nodefile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('fmm.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile_fmm+'\n')
        f.write(sigfile_fmm+'\n')
        f.write(outfile_fmm+'\n')
        f.write(invfile_fmm+'\n')
        f.write(refsig_fmm+'\n')
    
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d,'-fmm',str(nproc)],stdout=f)
        process.wait()
    
    if os.path.isfile('fmm.log'):
        with open('fmm.log','r') as f:
            if 'Cannot find the specified mesh node file: %s'%nodefile in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('fmm.inp',wdir+'/Req_%s.%d/fmm.inp'%(tag,cnt))
    mymove('fmm.log',wdir+'/Req_%s.%d/fmm.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    mymove('fmm_copy.inp','fmm.inp')
    mymove('fmm_copy.log','fmm.log')
    mymove('run_copy.log','run.log')
    return

def valid_mshfile(tag):
    cnt=0
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    sigfile='\'average\''
    refsig='none'
    mycopyfile('e4d.inp','e4d_copy.inp')
    mycopyfile('e4d.log','e4d_copy.log')
    mycopyfile('run.log','run_copy.log')

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: A mesh node file that was not in the directory was input in e4d.inp'%(tag,cnt)+\
    '\n... Cannot find the specified mesh node file: %s'%nodefile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'Cannot find the specified mesh node file: %s'%nodefile in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    mymove('e4d_copy.inp','e4d.inp')
    mymove('e4d_copy.log','e4d.log')
    mymove('run_copy.log','run.log')
    return

def valid_srvfile_fmm(tag):
    cnt=0
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    nodefile='borehole.1.node'
    sigfile_fmm='10'
    refsig_fmm='none'
    mycopyfile('fmm.inp','fmm_copy.inp')
    mycopyfile('fmm.log','fmm_copy.log')
    mycopyfile('run.log','run_copy.log')
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: A survey file that was not in the directory was input in fmm.inp'%(tag,cnt)+\
    '\n... Can\'t find the survey file: %s'%srvfile_fmm
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('fmm.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile_fmm+'\n')
        f.write(sigfile_fmm+'\n')
        f.write(outfile_fmm+'\n')
        f.write(invfile_fmm+'\n')
        f.write(refsig_fmm+'\n')
    
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d,'-fmm',str(nproc)],stdout=f)
        process.wait()
    
    if os.path.isfile('fmm.log'):
        with open('fmm.log','r') as f:
            if 'Can\'t find the survey file: %s'%srvfile_fmm in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('fmm.inp',wdir+'/Req_%s.%d/fmm.inp'%(tag,cnt))
    mymove('fmm.log',wdir+'/Req_%s.%d/fmm.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
        
    mymove('fmm_copy.inp','fmm.inp')
    mymove('fmm_copy.log','fmm.log')
    mymove('run_copy.log','run.log')
    return

def valid_srvfile(tag):
    cnt=0
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    nodefile='two_blocks.1.node'
    sigfile='\'average\''
    refsig='none'
    mycopyfile('e4d.inp','e4d_copy.inp')
    mycopyfile('e4d.log','e4d_copy.log')
    mycopyfile('run.log','run_copy.log')
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: A survey file that was not in the directory was input in e4d.inp'%(tag,cnt)+\
    '\n... Can\'t find the survey file: %s'%srvfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'Can\'t find the survey file: %s'%srvfile in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    if False: #continue from here
        cnt=cnt+1
        msg='Requirement %s.%d: An IMI survey file (IMI) does not contain electrodes with negative flags '%(tag,cnt)+\
        '\n... Can\'t find the survey file: %s'%srvfile
        print('')
        print_splitter('Test E4D Error handling','=',80)
        print(msg)

        with open('e4d.inp','w') as f:
            f.write('3\n')
            f.write(nodefile+'\n')
            f.write(srvfile+'\n')
            f.write(sigfile+'\n')
            f.write(outfile+'\n')
            f.write(invfile+'\n')
            f.write(refsig+'\n')

        with open('run.log','w') as f:
            process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
            process.wait()

        if os.path.isfile('e4d.log'):
            with open('e4d.log','r') as f:
                if 'Can\'t find the survey file: %s'%srvfile in f.read():
                    print('Success: E4D reported error and exited cleanly')
                else:
                    print('Failed: Error was not captured by E4D')
                    sys.stderr.write(msg+'\nE4D failed to report error\n')
        else:
            print('Failed: E4D was not ran successfully')
            sys.stderr.write(msg+'\nE4D failed to run\n')

        mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
        mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
        mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
        mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    mymove('e4d_copy.inp','e4d.inp')
    mymove('e4d_copy.log','e4d.log')
    mymove('run_copy.log','run.log')
    return

def valid_sigfile_fmm(tag):
    cnt=0
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    nodefile='borehole.1.node'
    srvfile_fmm='borehole.srv'
    refsig_fmm='none'
    mycopyfile('fmm.inp','fmm_copy.inp')
    mycopyfile('fmm.log','fmm_copy.log')
    mycopyfile('run.log','run_copy.log')
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: A slowness file that was not in the directory was input in fmm.inp'%(tag,cnt)+\
    '\n... Can\'t find the slowness file: %s'%sigfile_fmm
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('fmm.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile_fmm+'\n')
        f.write(sigfile_fmm+'\n')
        f.write(outfile_fmm+'\n')
        f.write(invfile_fmm+'\n')
        f.write(refsig_fmm+'\n')
    
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d,'-fmm',str(nproc)],stdout=f)
        process.wait()
    
    if os.path.isfile('fmm.log'):
        with open('fmm.log','r') as f:
            if 'Can\'t find the slowness file: %s'%sigfile_fmm in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('fmm.inp',wdir+'/Req_%s.%d/fmm.inp'%(tag,cnt))
    mymove('fmm.log',wdir+'/Req_%s.%d/fmm.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    mymove('fmm_copy.inp','fmm.inp')
    mymove('fmm_copy.log','fmm.log')
    mymove('run_copy.log','run.log')
    return

def valid_sigfile(tag):
    cnt=0
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    nodefile='two_blocks.1.node'
    srvfile='two_blocks.srv'
    refsig='none'
    mycopyfile('e4d.inp','e4d_copy.inp')
    mycopyfile('e4d.log','e4d_copy.log')
    mycopyfile('run.log','run_copy.log')
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: A conductivity file that was not in the directory was input in e4d.inp'%(tag,cnt)+\
    '\n... Can\'t find the conductivity file: %s'%sigfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'Can\'t find the conductivity file: %s'%sigfile in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    mymove('e4d_copy.inp','e4d.inp')
    mymove('e4d_copy.log','e4d.log')
    mymove('run_copy.log','run.log')
    return

def valid_outfile(tag):
    cnt=0
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    sigfile='\'average\''
    refsig='none'
    mycopyfile('e4d.inp','e4d_copy.inp')
    mycopyfile('e4d.log','e4d_copy.log')
    mycopyfile('run.log','run_copy.log')
    #E4D did not terminate if the output options file was not found
    #E4D did not terminate if there was a problem reading the first line in the output file
    #E4D did not terminate if there was a problem reading the predicted data file in: two_blocks.out
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if the output options file exists'%(tag,cnt)+\
    '\n... Cannot find the output options file '+outfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    myremove(outfile)
    with open(outfile,'w') as f:
        f.write('1\n')
        f.write('two_blocks.dpd\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'Cannot find the output options file: '+outfile in f.read():
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check the output options file format'%(tag,cnt)+\
    '\n... There was a problem reading the first line in the output file '+outfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(outfile,'w') as f:
        f.write('')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'The was a problem reading the first line in the output file: '+outfile in f.read():
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mymove(outfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check the output options file format'%(tag,cnt)+\
    '\n... There was a problem reading the predicted data file in '+outfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(outfile,'w') as f:
        f.write('1\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'The was a problem reading the predicted data file in: '+outfile in f.read():
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mymove(outfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check the output options file format'%(tag,cnt)+\
    '\n... There was a problem reading the predicted data file in '+outfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(outfile,'w') as f:
        f.write('1\n')
        f.write('two_blocks.dpd\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'The was a problem reading the predicted data file in: '+outfile in f.read():
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    mymove(outfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,outfile))
    
    mymove('e4d_copy.inp','e4d.inp')
    mymove('e4d_copy.log','e4d.log')
    mymove('run_copy.log','run.log')
    return

def valid_invfile(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    sigfile='\'average\''
    refsig='none'
    mycopyfile('e4d.inp','e4d_copy.inp')
    mycopyfile('e4d.log','e4d_copy.log')
    mycopyfile('run.log','run_copy.log')
    mycopyfile(invfile,invfile.split('.')[0]+'_copy.inv')
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if the inverse option file exists'%(tag,cnt)+\
    '\n... Cannot find the inverse options file '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    myremove(invfile)
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'Cannot find the inverse options file: '+invfile in f.read():
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    #mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    #mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    #mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    #mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... There was a problem reading the number of constraint in '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading the number of constraint' in f.read():
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    #cnt=cnt+1
    #msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    #'\n... There was a problem reading the number of constraint in '+invfile
    #print('')
    #print_splitter('Test E4D Error handling','=',80)
    #print(msg)
    
    #with open('e4d.inp','w') as f:
    #    f.write('3\n')
    #    f.write(nodefile+'\n')
    #    f.write(srvfile+'\n')
    #    f.write(sigfile+'\n')
    #    f.write(outfile+'\n')
    #    f.write(invfile+'\n')
    #    f.write(refsig+'\n')
    #with open(invfile,'w') as f:
    #    f.write('1.l\n')

    #with open('run.log','w') as f:
    #    process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
    #    process.wait()
        
    #with open('e4d.log','r') as f:
    #    if 'There was a problem reading the number of constraint' in f.read():
    #        print('Success: E4D reported error and exited cleanly')
    #    else:
    #        print('Failed: Error was not captured by E4D')
    #        sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    #mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    #mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    #mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    #mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    #mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... There was a problem reading the zone number'+\
    '\n... for constraint block 1 in '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading the zone number'+\
        '  for constraint block            1 .'+\
        '  Check the inverse options file: '+invfile in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    #cnt=cnt+1
    #msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    #'\n... There was a problem reading the zone number'+\
    #'\n... for constraint block 1 in '+invfile
    #print('')
    #print_splitter('Test E4D Error handling','=',80)
    #print(msg)
    
    #with open('e4d.inp','w') as f:
    #    f.write('3\n')
    #    f.write(nodefile+'\n')
    #    f.write(srvfile+'\n')
    #    f.write(sigfile+'\n')
    #    f.write(outfile+'\n')
    #    f.write(invfile+'\n')
    #    f.write(refsig+'\n')
    #with open(invfile,'w') as f:
    #    f.write('1\n')
    #    f.write('11.1\n')

    #with open('run.log','w') as f:
    #    process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
    #    process.wait()
        
    #with open('e4d.log','r') as f:
    #    if 'There was a problem reading the zone number'+\
    #    '  for constraint block            1 .'+\
    #    '  Check the inverse options file: '+invfile in f.read().replace('\n',''):
    #        print('Success: E4D reported error and exited cleanly')
    #    else:
    #        print('Failed: Error was not captured by E4D')
    #        sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    #mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    #mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    #mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    #mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    #mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... There was a problem reading either the structure metric'+\
    '\n... or the spatial weights for constraint block 1 in '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading either the structure metric'+\
        '  or the spatial weights for constraint block            1' in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    #cnt=cnt+1
    #msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    #'\n... There was a problem reading either the structure metric'+\
    #'\n... or the spatial weights for constraint block 1 in '+invfile
    #print('')
    #print_splitter('Test E4D Error handling','=',80)
    #print(msg)
    
    #with open('e4d.inp','w') as f:
    #    f.write('3\n')
    #    f.write(nodefile+'\n')
    #    f.write(srvfile+'\n')
    #    f.write(sigfile+'\n')
    #    f.write(outfile+'\n')
    #    f.write(invfile+'\n')
    #    f.write(refsig+'\n')
    #with open(invfile,'w') as f:
    #    f.write('1\n\n')
    #    f.write('11\n')
    #    f.write('2.1 -1 -1 -1\n')

    #with open('run.log','w') as f:
    #    process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
    #    process.wait()
        
    #with open('e4d.log','r') as f:
    #    if 'There was a problem reading either the structure metric'+\
    #    '  or the spatial weights for constraint block            1' in f.read().replace('\n',''):
    #        print('Success: E4D reported error and exited cleanly')
    #    else:
    #        print('Failed: Error was not captured by E4D')
    #        sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    #mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    #mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    #mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    #mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    #mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... There was a problem reading either the reweighting function'+\
    '\n... or the reweighting function parameters for constraint block 1 in '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('2 1 1 1\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading either the reweighting function'+\
        '  or the reweighting function parameters for constraint block            1' in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    #cnt=cnt+1
    #msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    #'\n... There was a problem reading either the reweighting function'+\
    #'\n... or the reweighting function parameters for constraint block 1 in '+invfile
    #print('')
    #print_splitter('Test E4D Error handling','=',80)
    #print(msg)
    
    #with open('e4d.inp','w') as f:
    #    f.write('3\n')
    #    f.write(nodefile+'\n')
    #    f.write(srvfile+'\n')
    #    f.write(sigfile+'\n')
    #    f.write(outfile+'\n')
    #    f.write(invfile+'\n')
    #    f.write(refsig+'\n')
    #with open(invfile,'w') as f:
    #    f.write('1\n\n')
    #    f.write('11\n')
    #    f.write('2 1 1 1\n')
    #    f.write('1.1 10 0.01\n')

    #with open('run.log','w') as f:
    #    process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
    #    process.wait()
        
    #with open('e4d.log','r') as f:
    #    if 'There was a problem reading either the reweighting function'+\
    #    '  or the reweighting function parameters for constraint block            1' in f.read().replace('\n',''):
    #        print('Success: E4D reported error and exited cleanly')
    #    else:
    #        print('Failed: Error was not captured by E4D')
    #        sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    #mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    #mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    #mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    #mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    #mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... There was a problem reading the zone links'+\
    '\n... for constraint block 1 in '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('2 1 1 1\n')
        f.write('1 10 0.01\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading the zone links'+\
        '  for constraint block            1' in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    #cnt=cnt+1
    #msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    #'\n... There was a problem reading the zone links'+\
    #'\n... for constraint block 1 in '+invfile
    #print('')
    #print_splitter('Test E4D Error handling','=',80)
    #print(msg)
    
    #with open('e4d.inp','w') as f:
    #    f.write('3\n')
    #    f.write(nodefile+'\n')
    #    f.write(srvfile+'\n')
    #    f.write(sigfile+'\n')
    #    f.write(outfile+'\n')
    #    f.write(invfile+'\n')
    #    f.write(refsig+'\n')
    #with open(invfile,'w') as f:
    #    f.write('1\n\n')
    #    f.write('11\n')
    #    f.write('2 1 1 1\n')
    #    f.write('1 10 0.01\n')
    #    f.write('1.1 2\n')

    #with open('run.log','w') as f:
    #    process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
    #    process.wait()
        
    #with open('e4d.log','r') as f:
    #    if 'There was a problem reading the zone links'+\
    #    '  for constraint block            1' in f.read().replace('\n',''):
    #        print('Success: E4D reported error and exited cleanly')
    #    else:
    #        print('Failed: Error was not captured by E4D')
    #        sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    #mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    #mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    #mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    #mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    #mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... There was a problem reading the reference'+\
    '\n... for constraint block 1 in '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('2 1 1 1\n')
        f.write('1 10 0.01\n')
        f.write('1 2\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading the reference'+\
        '  for constraint block            1' in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... There was a problem reading the relative weight'+\
    '\n... for constraint block 1 in '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('2 1 1 1\n')
        f.write('1 10 0.01\n')
        f.write('1 2\n')
        f.write('0\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading the relative weight'+\
        '  for constraint block            1' in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... Structural metrics 12 is for joint inversion'+\
    '\n... of travel time and resistivity data, and require both'+\
    '\n... E4D and FMM to be running in inverse mode'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('12 1 1 1\n') #structural metric should between 0 and 13
        f.write('1 10 0.01\n')
        f.write('1 2\n')
        f.write('0\n')
        f.write('1\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'Structural metrics 12 and 13 are for joint inversion'+\
        ' of travel time and resistivity data, and require both'+\
        ' E4D and FMM to be running in inverse mode' in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... Structural metrics 13 is for joint inversion'+\
    '\n... of travel time and resistivity data, and require both'+\
    '\n... E4D and FMM to be running in inverse mode'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('13 1 1 1\n') #structural metric should between 0 and 13
        f.write('1 10 0.01\n')
        f.write('1 2\n')
        f.write('0\n')
        f.write('1\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'Structural metrics 12 and 13 are for joint inversion'+\
        ' of travel time and resistivity data, and require both'+\
        ' E4D and FMM to be running in inverse mode' in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... Invalid structural metric (-1) in the inverse options file '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('-1 1 1 1\n') #structural metric should between 0 and 13
        f.write('1 10 0.01\n')
        f.write('1 2\n')
        f.write('0\n')
        f.write('1\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'Invalid structural metric' in f.read():
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... Invalid structural metric (14) in the inverse options file '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('14 1 1 1\n') #structural metric should between 0 and 13
        f.write('1 10 0.01\n')
        f.write('1 2\n')
        f.write('0\n')
        f.write('1\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'Invalid structural metric' in f.read():
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... Invalid reweighting function (0) in the inverse options file '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('2 1 1 1\n')
        f.write('0 10 0.01\n') #re-weighting function should between 1 and 99
        f.write('1 2\n')
        f.write('0\n')
        f.write('1\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'Invalid reweighting function' in f.read():
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
        
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... Invalid reweighting function (100) in the inverse options file '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('2 1 1 1\n')
        f.write('100 10 0.01\n') #re-weighting function should between 1 and 99
        f.write('1 2\n')
        f.write('0\n')
        f.write('1\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'Invalid reweighting function' in f.read():
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... There was a problem reading the global starting constraint weight '+\
    '\n... (beta) line in the inversion options file in '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('2 1 1 1\n')
        f.write('1 10 0.01\n')
        f.write('1 2\n')
        f.write('0\n')
        f.write('1\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading the global starting constraint weight'+\
        '  (beta) line in the inversion options file: '+invfile in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... There was a problem reading the target chi-squared value'+\
    '\n... in '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('2 1 1 1\n')
        f.write('1 10 0.01\n')
        f.write('1 2\n')
        f.write('0\n')
        f.write('1\n\n')
        f.write('100 0.25 0.5\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading the target chi-squared value'+\
        '  in: '+invfile in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... There was a problem reading the minimum and maximum number of inner'+\
    '\n... iterations in the inverse options file '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('2 1 1 1\n')
        f.write('1 10 0.01\n')
        f.write('1 2\n')
        f.write('0\n')
        f.write('1\n\n')
        f.write('100 0.25 0.5\n')
        f.write('1.0\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading the maximum number of inner'+\
        '  iterations in the inverse options file: '+invfile in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... There was a problem reading the max and min'+\
    '\n... conductivities in the inverse options file '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('2 1 1 1\n')
        f.write('1 10 0.01\n')
        f.write('1 2\n')
        f.write('0\n')
        f.write('1\n\n')
        f.write('100 0.25 0.5\n')
        f.write('1.0\n')
        f.write('30 50\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading the max and min'+\
        '  conductivities in the inverse options file: '+invfile in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... There was a problem reading the update option'+\
    '\n... in the inverse options file '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('2 1 1 1\n')
        f.write('1 10 0.01\n')
        f.write('1 2\n')
        f.write('0\n')
        f.write('1\n\n')
        f.write('100 0.25 0.5\n')
        f.write('1.0\n')
        f.write('30 50\n')
        f.write('1e-5 1.0\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading the update option'+\
        '  in the inverse options file: '+invfile in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check inverse option file format'%(tag,cnt)+\
    '\n... There was a problem reading the data culling options'+\
    '\n... in the inverse options file '+invfile
    print('')
    print_splitter('Test E4D Error handling','=',80)
    print(msg)
    
    with open('e4d.inp','w') as f:
        f.write('3\n')
        f.write(nodefile+'\n')
        f.write(srvfile+'\n')
        f.write(sigfile+'\n')
        f.write(outfile+'\n')
        f.write(invfile+'\n')
        f.write(refsig+'\n')
    with open(invfile,'w') as f:
        f.write('1\n\n')
        f.write('11\n')
        f.write('2 1 1 1\n')
        f.write('1 10 0.01\n')
        f.write('1 2\n')
        f.write('0\n')
        f.write('1\n\n')
        f.write('100 0.25 0.5\n')
        f.write('1.0\n')
        f.write('30 50\n')
        f.write('1e-5 1.0\n')
        f.write('2\n')

    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
        
    with open('e4d.log','r') as f:
        if 'There was a problem reading the data culling options '+\
        '  in the inverse options file: '+invfile in f.read().replace('\n',''):
            print('Success: E4D reported error and exited cleanly')
        else:
            print('Failed: Error was not captured by E4D')
            sys.stderr.write(msg+'\nE4D failed to report error\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mymove('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mymove(invfile,wdir+'/Req_%s.%d/%s'%(tag,cnt,invfile))
    mymove('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mymove('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    mymove('e4d_copy.inp','e4d.inp')
    mymove('e4d_copy.log','e4d.log')
    mymove('run_copy.log','run.log')
    mycopyfile(invfile.split('.')[0]+'_copy.inv',invfile)
    return

def valid_nproc(tag):
    cnt=-1
    wdir=os.path.join(root,'Req_'+tag)
    myrmtree(wdir)
    mymkdir(wdir)
    
    mycopyfile('e4d.inp','e4d_copy.inp')
    mycopyfile('e4d.log','e4d_copy.log')
    mycopyfile('run.log','run_copy.log')
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: Check if the primary input file e4d.inp exists'%(tag,cnt)
    print('')
    if tag.split('.')[0]==3:
        print_splitter('Test Forward Simulation Mode','=',80)
    else:
        print_splitter('Test Inversion Mode','=',80)
    print(msg)
    
    if os.path.isfile('e4d.inp'):
        print('Success: e4d.inp was found')
    else:
        print('Failed: The primary input file was not found')
        sys.stderr.write(msg+'\nMPI test failed\n')
        return
    
    with open('e4d.inp') as f:
        mode=f.readline().split()[0]
    
    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: The number of processors is not correct in mode %s'%(tag,cnt,mode)+\
    '\n... E4D requires at least 2 processors to run in mode %s'%mode
    print('')
    print_splitter('Test E4D Error handling','=',80)
    #if tag.split('.')[0]==3:
    #    print_splitter('Test Forward Simulation Mode','=',80)
    #else:
    #    print_splitter('Test Inversion Mode','=',80)
    print(msg)
    
    nproc=1
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'E4D requires at least 2 processors to run in modes greater than 1' in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))

    #====================================================================================================
    cnt=cnt+1
    msg='Requirement %s.%d: The number of processors is not correct in mode %s'%(tag,cnt,mode)+\
    '\n... The number of processors minus 1 must not exceed the number electrodes'
    print('')
    print_splitter('Test E4D Error handling','=',80)
    #if tag.split('.')[0]==3:
    #    print_splitter('Test Forward Simulation Mode','=',80)
    #else:
    #    print_splitter('Test Inversion Mode','=',80)
    print(msg)
        
    nproc=50
    with open('run.log','w') as f:
        process=subprocess.Popen([mpirun,'-np',str(nproc),e4d],stdout=f)
        process.wait()
    
    if os.path.isfile('e4d.log'):
        with open('e4d.log','r') as f:
            if 'The number of processors minus 1 must not exceed the number electrodes' in f.read():
                print('Success: E4D reported error and exited cleanly')
            else:
                print('Failed: Error was not captured by E4D')
                sys.stderr.write(msg+'\nE4D failed to report error\n')
    else:
        print('Failed: E4D was not ran successfully')
        sys.stderr.write(msg+'\nE4D failed to run\n')
    
    mymkdir(wdir+'/Req_%s.%d'%(tag,cnt))
    mycopyfile('e4d.inp',wdir+'/Req_%s.%d/e4d.inp'%(tag,cnt))
    mycopyfile('e4d.log',wdir+'/Req_%s.%d/e4d.log'%(tag,cnt))
    mycopyfile('run.log',wdir+'/Req_%s.%d/run.log'%(tag,cnt))
    
    mymove('e4d_copy.inp','e4d.inp')
    mymove('e4d_copy.log','e4d.log')
    mymove('run_copy.log','run.log')
    return

def mycopyfile(src,dst):
    try:
        shutil.copyfile(src,dst)
    except Exception as e:
        print('')
        print('Warning: Unable to copy file %s'%src)
    return

def mycopytree(src,dst):
    try:
        shutil.copytree(src,dst)
    except Exception as e:
        print('')
        print('Warning: Unable to copy directory %s'%src)
    return

def mymove(src,dst):
    try:
        shutil.move(src,dst)
    except Exception as e:
        print('')
        print('Warning: Unable to move file or directory %s'%src)
    return

def myrmtree(dirname):
    try:
        shutil.rmtree(dirname)
    except Exception as e:
        print('')
        print('Warning: Unable to delete directory %s'%dirname)
    return

def mymkdir(dirname):
    try:
        os.mkdir(dirname)
    except Exception as e:
        print('')
        print('Warning: Unable to create directory %s'%dirname)
    return

def myremove(filename):
    try:
        os.remove(filename)
    except Exception as e:
        print('')
        print('Warning: Unable to remove file %s'%filename)
    return

def replace_line(fname,old,new):
    with open(fname,'r+') as f:
        lines=f.readlines()
        for il in range(len(lines)):
            if lines[il][:len(old)]==old:
                junk=lines[il][len(old):]
                lines[il]=new+junk
                break
        #f.seek(0)
        #f.writelines(lines)
    
    with open(fname,'w') as f:
        f.writelines(lines)
    return

def print_splitter(text,symbol,width):
    width=max(len(text)+2,width)
    cwidth=len(text)+2
    lwidth=int((width-cwidth)/2)
    rwidth=int(width-cwidth-lwidth)
    print(symbol*lwidth+' '+text+' '+symbol*rwidth)
    return

def sort_folders(prefix):
    myrmtree(root+'/%s'%prefix)
    mymkdir(root+'/%s'%prefix)
    cnt=0
    while True:
        cnt=cnt+1
        if os.path.isdir(root+'/%s.%d'%(prefix,cnt)):
            mymove(root+'/%s.%d'%(prefix,cnt),root+'/%s'%prefix)
        else:
            break
    return

def get_mshcfg(cfgfile):
    global mbot,ncpts,cpts,nplc,plc,plclist,nholes,holes,nzones,zones
    
    with open('e4d.inp') as f:
        mode=f.readline().split()[0]
    
    mbot=float('nan')
    ncpts=-999
    cpts=np.zeros((0,5))
    nplc=-999
    plc=np.zeros((0,2))
    plclist=[]
    nholes=-999
    holes=np.zeros((0,4))
    nzones=-999
    zones=np.zeros((0,7))
    
    linnum=0
    lincnt=0
    with open(cfgfile) as f:
        for line in f:
            linnum=linnum+1
            if len(line.split())==0:
                continue
            lincnt=lincnt+1

            if lincnt==1:
                if not isfloat(line.split()[0]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: mesh quality was not a number')
                    f.close()
                    return False
                if len(line.split())<2:
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: missing max volume in mesh configuration')
                    f.close()
                    return False
                if not isfloat(line.split()[1]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: max volume was not a number')
                    f.close()
                    return False

            elif lincnt==2:
                if not isfloat(line.split()[0]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: bottom of mesh elevation was not a number')
                    f.close()
                    return False

                mbot=float(line.split()[0])

            elif lincnt==3:
                if not isint(line.split()[0]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: flag to build mesh was not an integer')
                    f.close()
                    return False
                if int(line.split()[0])<0 or int(line.split()[0])>1:
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: flag to build mesh was not 0 or 1')
                    f.close()
                    return False

            elif lincnt==4:
                if not os.path.isfile(line.split()[0][1:-1]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: tetgen path was not correct')
                    f.close()
                    return False
                tetgen=line.split()[0][1:-1]

            elif lincnt==5:
                if not os.path.isfile(line.split()[0][1:-1]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: triangle path was not correct')
                    f.close()
                    return False
                triangle=line.split()[0][1:-1]

            elif lincnt==6:
                if not isint(line.split()[0]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: number of control points was not an integer')
                    f.close()
                    return False
                ncpts=int(line.split()[0])
                cpts=np.zeros((ncpts,5))

            elif lincnt <= ncpts+6:
                if not isint(line.split()[0]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: control point index was not an integer')
                    f.close()
                    return False
                if lincnt!=int(line.split()[0])+6:
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: control point index was not continous')
                    f.close()
                    return False
                if len(line.split())<5:
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: missing coordinates or boundary flag of the control point')
                    f.close()
                    return False
                for i in range(3):
                    if not isfloat(line.split()[i+1]):
                        print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                        print('Error: control point coordintes were not numbers')
                        f.close()
                        return False
                if not isint(line.split()[4]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: control point boundary flag was not an integer')
                    f.close()
                    return False
                cpts[lincnt-7,0]=int(line.split()[0])
                cpts[lincnt-7,1]=float(line.split()[1])
                cpts[lincnt-7,2]=float(line.split()[2])
                cpts[lincnt-7,3]=float(line.split()[3])
                cpts[lincnt-7,4]=int(line.split()[4])

            elif lincnt==ncpts+7:
                if not isint(nplc):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: number of internal planes was not an integer')
                    f.close()
                    return False
                nplc=int(line.split()[0])
                plc=np.zeros((nplc,2))

            elif lincnt <= nplc*2+ncpts+7:
                if (lincnt-ncpts-7)%2:
                    if not isint(line.split()[0]):
                        print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                        print('Error: number of PLC points was not an integer')
                        f.close()
                        return False
                    if len(line.split())<2:
                        print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                        print('Error: missing PLC boundary number')
                        f.close()
                        return False
                    if not isint(line.split()[1]):
                        print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                        print('Error: PLC boundary number was not an integer')
                        f.close()
                        return False
                    if int(line.split()[1])==1 or int(line.split()[1])==2:
                        print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                        print('Error: PLC boundary number was 1 or 2')
                        return False
                    ncpts_on_plc=int(line.split()[0])
                    plc[int((lincnt-ncpts-8)/2),0]=int(line.split()[0])
                    plc[int((lincnt-ncpts-8)/2),1]=int(line.split()[1])
                else:        
                    if len(line.split())<ncpts_on_plc:
                        print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                        print('Error: missing PLC points')
                        f.close()
                        return False
                    plclist.append(np.zeros(ncpts_on_plc))
                    for i in range(ncpts_on_plc):
                        if not isint(line.split()[i]):
                            print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                            print('Error: PLC point index was not an integer')
                            f.close()
                            return False
                        if int(line.split()[i])<1 or int(line.split()[i])>ncpts:
                            print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                            print('Error: PLC point index was out of range')
                            f.close()
                            return False
                        plclist[-1][i]=int(line.split()[i])

            elif lincnt==nplc*2+ncpts+8:
                if not isint(line.split()[0]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: number of holes was not an integer')
                    f.close()
                    return False
                nholes=int(line.split()[0])
                holes=np.zeros((nholes,4))

            elif lincnt <= nholes+nplc*2+ncpts+8:
                if not isint(line.split()[0]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: hole index was not an integer')
                    f.close()
                    return False
                #if lincnt!=int(line.split()[0])+nplc*2+ncpts+8:
                #    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                #    print('Error: hole index was not continuous')
                #    f.close()
                #    return False
                if len(line.split())<4:
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: missing numbers in hole configuration')
                    f.close()
                    return False
                for i in range(3):
                    if not isfloat(line.split()[i+1]):
                        print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                        print('Error: coordinates of point in the hole were not numbers')
                        f.close()
                        return False
                holes[lincnt-nplc*2-ncpts-9,0]=int(line.split()[0])
                holes[lincnt-nplc*2-ncpts-9,1]=float(line.split()[1])
                holes[lincnt-nplc*2-ncpts-9,2]=float(line.split()[2])
                holes[lincnt-nplc*2-ncpts-9,3]=float(line.split()[3])

            elif lincnt==nholes+nplc*2+ncpts+9:
                if not isint(line.split()[0]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: number of zones was not an integer')
                    f.close()
                    return False
                nzones=int(line.split()[0])
                zones=np.zeros((nzones,7))

            elif lincnt <= nzones+nholes+nplc*2+ncpts+9:
                if not isint(line.split()[0]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: zone index was not an integer')
                    f.close()
                    return False
                if lincnt!=int(line.split()[0])+nholes+nplc*2+ncpts+9:
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: zone index was not continous')
                    f.close()
                    return False
                if len(line.split())<6:
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: missing numbers in zone configuration')
                    f.close()
                    return False
                for i in range(3):
                    if not isfloat(line.split()[i+1]):
                        print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                        print('Error: coordinates of point in the zone were not numbers')
                        f.close()
                        return False
                if not isfloat(line.split()[4]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: max volume of elements in the zone was not a number')
                    f.close()
                    return False
                if not isfloat(line.split()[5]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: conductivity of the zone was not a number')
                    f.close()
                    return False
                zones[lincnt-nholes-nplc*2-ncpts-10,0]=int(line.split()[0])
                zones[lincnt-nholes-nplc*2-ncpts-10,1]=float(line.split()[1])
                zones[lincnt-nholes-nplc*2-ncpts-10,2]=float(line.split()[2])
                zones[lincnt-nholes-nplc*2-ncpts-10,3]=float(line.split()[3])
                zones[lincnt-nholes-nplc*2-ncpts-10,4]=float(line.split()[4])
                zones[lincnt-nholes-nplc*2-ncpts-10,5]=float(line.split()[5])
                if mode=='21' or mode=='SIP1' or mode=='41' or mode=='SIPtank1':
                    zones[lincnt-nholes-nplc*2-ncpts-10,6]=float(line.split()[6])
            
            elif lincnt==nzones+nholes+nplc*2+ncpts+10:
                if not isint(line.split()[0]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: flag to build exodus file was not an integer')
                    f.close()
                    return False
                if int(line.split()[0])<0 or int(line.split()[0])>1:
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: flag to build exodus file was not 0 or 1')
                    f.close()
                    return False

            elif lincnt==nzones+nholes+nplc*2+ncpts+11:
                if not os.path.isfile(line.split()[0][1:-1]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: bx path was not correct')
                    f.close()
                    return False
                bx=line.split()[0][1:-1]

            elif lincnt==nzones+nholes+nplc*2+ncpts+12:
                if not isint(line.split()[0]):
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: flag to translate the mesh was not an integer')
                    f.close()
                    return False
                if int(line.split()[0])<0 or int(line.split()[0])>1:
                    print('Last read (%s line %d): %s'%(cfgfile,linnum,line[:-1]))
                    print('Error: flag to translate the mesh was not 0 or 1')
                    f.close()
                    return False
    
    return

def get_sigma(sigfile):
    with open(sigfile) as f:
        nele=int(f.readline().split()[0])
        sigma=np.zeros(nele)
        for i in range(nele):
            sigma[i]=float(f.readline().split()[0])
    return sigma

def get_nodes(nodefile,trnfile):
    if os.path.isfile(trnfile):
        trn=np.loadtxt(trnfile)
    else:
        trn=np.zeros(3)
    with open(nodefile) as f:
        nnode=int(f.readline().split()[0])
        nodes=np.zeros((nnode,5))
        for i in range(nnode):
            line=f.readline()
            nodes[i,0]=float(line.split()[1])+trn[0]
            nodes[i,1]=float(line.split()[2])+trn[1]
            nodes[i,2]=float(line.split()[3])+trn[2]
            nodes[i,3]=int(line.split()[4])
            nodes[i,4]=int(line.split()[5])
    return nodes

def get_survey(srvfile):
    lincnt=0
    with open(srvfile) as f:
        for line in f:
            if not len(line.split()):
                continue
            lincnt=lincnt+1
            if lincnt==1:
                ne=int(line.split()[0])
                epos=np.zeros((ne,4))
            elif lincnt <= ne+1:
                epos[lincnt-2,0]=float(line.split()[1])
                epos[lincnt-2,1]=float(line.split()[2])
                epos[lincnt-2,2]=float(line.split()[3])
                epos[lincnt-2,3]=int(float(line.split()[4]))
            elif lincnt==ne+2:
                na=int(line.split()[0])
                ecfg=np.zeros((na,6))
            elif lincnt <= na+ne+2:
                ecfg[lincnt-ne-3,0]=int(line.split()[1])
                ecfg[lincnt-ne-3,1]=int(line.split()[2])
                ecfg[lincnt-ne-3,2]=int(line.split()[3])
                ecfg[lincnt-ne-3,3]=int(line.split()[4])
                ecfg[lincnt-ne-3,4]=float(line.split()[5])
                ecfg[lincnt-ne-3,5]=float(line.split()[6])
    return epos,ecfg

def get_dpred(dpdfile):
    with open(dpdfile) as f:
        na=int(f.readline().split()[0])
        dpred=np.zeros((na,6))
        for i in range(na):
            line=f.readline()
            dpred[i,0]=int(line.split()[1])
            dpred[i,1]=int(line.split()[2])
            dpred[i,2]=int(line.split()[3])
            dpred[i,3]=int(line.split()[4])
            dpred[i,4]=float(line.split()[5])
            dpred[i,5]=float(line.split()[6])
    return dpred

def get_potind(outfile):
    potind=[]
    if os.path.isfile(outfile):
        with open(outfile) as f:
            lines=f.readlines()
            if len(lines)>2:
                npot=int(lines[2].split()[0])
                for i in range(npot):
                    potind.append(int(lines[3+i].split()[0]))
    
    return potind

def get_gf(ei,ep,elev,rshift=False):
    if ep.ndim==1:
        r=np.sqrt((ei[0]-ep[0])**2+(ei[1]-ep[1])**2+(ei[2]-ep[2])**2)
        ri=np.sqrt((ei[0]-ep[0])**2+(ei[1]-ep[1])**2+(2*elev-ei[2]-ep[2])**2)
    else:
        r=np.sqrt((ei[0]-ep[:,0])**2+(ei[1]-ep[:,1])**2+(ei[2]-ep[:,2])**2)
        ri=np.sqrt((ei[0]-ep[:,0])**2+(ei[1]-ep[:,1])**2+(2*elev-ei[2]-ep[:,2])**2)
    if rshift:
        r=r+1e-15
        ri=ri+1e-15
    gf=1/r+1/ri
    return gf

def isclose(x,y,tol=1e-6):
    a=np.array(x).ravel()
    b=np.array(y).ravel()
    
    if len(a)<len(b):
        a=np.tile(a,len(b))
    elif len(b)<len(a):
        b=np.tile(b,len(a))
    
    out=np.zeros(len(a),dtype=bool)
    mask=(a==0)|(b==0)
    out[mask]=abs(a[mask]-b[mask])<tol
    out[~mask]=abs(a[~mask]-b[~mask])<tol*np.maximum(abs(a[~mask]),abs(b[~mask]))
    return out

def isint(x):
    try:
        a=float(x)
        b=int(a)
    except ValueError:
        return False
    else:
        return a==b

def isfloat(x):
    try:
        a=float(x)
    except ValueError:
        return False
    else:
        return True

if __name__=='__main__':
    run_tutorials('all')
    test_case('inputs')
    test_case('mesh')
    test_case('forward')
    test_case('inversion')
    
    test_case('px')
    
    print('')
    print('Done')
