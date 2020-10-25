#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# ######################################################################
# Cバイナリ=>Python変換モジュール
# 
# Ryota Shimokawara (sr17805@tomakomai.kosen-ac.jp)
# 2018
# ######################################################################

import subprocess, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) #このスクリプトのパス
mseq = SCRIPT_DIR+"/m14.DSB"

def playrec_mono(averaging_times, outfile):
    cmd=" ".join([SCRIPT_DIR+'/c_bin/playrec_mono_inPath', mseq, str(averaging_times), outfile, SCRIPT_DIR])
    subprocess.Popen(cmd.split(" ")).wait()

def playrec_2ch(averaging_times, outfile):
    cmd=" ".join([SCRIPT_DIR+'/c_bin/playrec_2ch_inPath', mseq, str(averaging_times), outfile, SCRIPT_DIR])
    subprocess.Popen(cmd.split(" ")).wait()

def averaging(infile, averaging_times, outfile):
    cmd=" ".join([SCRIPT_DIR+'/c_bin/douki_new', mseq, infile, str(averaging_times), outfile])
    subprocess.Popen(cmd.split(" ")).wait()

def cross_correlation(infile, outfile):
    cmd=" ".join([SCRIPT_DIR+'/c_bin/IMPmcode', mseq, infile, outfile])
    subprocess.Popen(cmd.split(" ")).wait()    

def unbias(file):
    cmd=" ".join([SCRIPT_DIR+'/c_bin/unbias', file, file])
    subprocess.Popen(cmd.split(" ")).wait()    

def trim(infile, start, end, outfile):
    cmd=" ".join([SCRIPT_DIR+'/c_bin/cutout_anyfile', infile, str(start), str(end), outfile])
    subprocess.Popen(cmd.split(" ")).wait()    

def inverse(infile, band_path_filter, outfile, tap_length):
    cmd=" ".join([SCRIPT_DIR+'/c_bin/inverse', infile, band_path_filter, outfile, str(tap_length)])
    subprocess.Popen(cmd.split(" ")).wait()    

def speach(division_number, infile):
    cmd=" ".join([SCRIPT_DIR+'/c_bin/sepach', str(division_number), infile])
    subprocess.Popen(cmd.split(" ")).wait() 

def closedloop():
    subprocess.Popen(SCRIPT_DIR+'/c_bin/closed_loop_new').wait() 