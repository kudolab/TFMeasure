#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# ######################################################################
# 伝達関数の測定とマイクの左右音圧調整用Pythonモジュール
# 
# Ryota Shimokawara (sr17805@tomakomai.kosen-ac.jp)
# 2018
# ######################################################################
# SSTF内にif文追加(53行), ITD_checkの分岐@2019.5.23
# ######################################################################

import os

from cpyconv import playrec_mono, playrec_2ch, averaging, cross_correlation, unbias, trim, inverse, speach

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # このスクリプトのパス
band_path_filter = SCRIPT_DIR + "/BPFBPFBPF100-13k_48k_0-255.DDB"


def LSTF(num, averaging_times, trim_imp_start, trim_imp_end, trim_inv_start, trim_inv_end, outdir):
    outdir = outdir + "/LSTF"
    if not os.path.exists(outdir): os.makedirs(outdir)
    playrec_mono(averaging_times, "/tmp/rec.DSB")
    averaging("/tmp/rec.DSB", averaging_times, "/tmp/tmp.DSB")
    cross_correlation("/tmp/tmp.DSB", outdir + "/LSTF_" + str(num) + ".DDA")
    unbias(outdir + "/LSTF_" + str(num) + ".DDA")
    trim(outdir + "/LSTF_" + str(num) + ".DDA", trim_imp_start, trim_imp_end, outdir + "/cLSTF_" + str(num) + ".DDB")
    inverse(outdir + "/cLSTF_" + str(num) + ".DDB", band_path_filter, outdir + "/inv_cLSTF_" + str(num) + ".DDB", 4096)
    trim(outdir + "/inv_cLSTF_" + str(num) + ".DDB", trim_inv_start, trim_inv_end,
         outdir + "/cinv_cLSTF_" + str(num) + ".DDB")


def RSTF(subject, averaging_times, trim_imp_start, trim_imp_end, trim_inv_start, trim_inv_end, subdir):
    outdir = subdir + "/RSTF"
    for dir in [subdir, outdir]:
        if not os.path.exists(dir): os.makedirs(dir)
    playrec_2ch(averaging_times, "/tmp/rec.DSB")
    speach(2, "/tmp/rec.DSB")
    averaging("/tmp/rec_1.DSB", averaging_times, "/tmp/tmp_L.DSB")
    averaging("/tmp/rec_2.DSB", averaging_times, "/tmp/tmp_R.DSB")
    for LR in ['L', 'R']:
        cross_correlation("/tmp/tmp_" + LR + ".DSB", outdir + "/RSTF_" + LR + ".DDA")
        unbias(outdir + "/RSTF_" + LR + ".DDA")
        trim(outdir + "/RSTF_" + LR + ".DDA", trim_imp_start, trim_imp_end, outdir + "/cRSTF_" + LR + ".DDB")
        inverse(outdir + "/cRSTF_" + LR + ".DDB", band_path_filter, outdir + "/inv_cRSTF_" + LR + ".DDB", 4096)
        trim(outdir + "/inv_cRSTF_" + LR + ".DDB", trim_inv_start, trim_inv_end, outdir + "/cinv_cRSTF_" + LR + ".DDB")


def SSTF(subject, averaging_times, angle, trim_imp_start, trim_imp_end, subdir):
    outdir = subdir + "/SSTF"
    for dir in [subdir, outdir]:
        if not os.path.exists(dir): os.makedirs(dir)
    playrec_2ch(averaging_times, "/tmp/rec.DSB")
    speach(2, "/tmp/rec.DSB")
    averaging("/tmp/rec_1.DSB", averaging_times, "/tmp/tmp_L.DSB")
    averaging("/tmp/rec_2.DSB", averaging_times, "/tmp/tmp_R.DSB")
    # 追加したif文
    if str(angle) == "check":  # 追加した行
        for LR in ['L', 'R']:
            cross_correlation("/tmp/tmp_" + LR + ".DSB", outdir + "/SSTF_check_" + LR + ".DDA")
            unbias(outdir + "/SSTF_check_" + LR + ".DDA")
            trim(outdir + "/SSTF_check_" + LR + ".DDA", trim_imp_start, trim_imp_end,
                 outdir + "/cSSTF_check_" + LR + ".DDB")
    else:
        for LR in ['L', 'R']:
            cross_correlation("/tmp/tmp_" + LR + ".DSB", outdir + "/SSTF_" + str(angle) + "_" + LR + ".DDA")
            unbias(outdir + "/SSTF_" + str(angle) + "_" + LR + ".DDA")
            trim(outdir + "/SSTF_" + str(angle) + "_" + LR + ".DDA", trim_imp_start, trim_imp_end,
                 outdir + "/cSSTF_" + str(angle) + "_" + LR + ".DDB")
    # ######################################################################
    # for LR in ['L', 'R']:
    #    cross_correlation("/tmp/tmp_"+LR+".DSB", outdir+"/SSTF_"+str(angle)+"_"+LR+".DDA")
    #    unbias(outdir+"/SSTF_"+str(angle)+"_"+LR+".DDA")
    #    trim(outdir+"/SSTF_"+str(angle)+"_"+LR+".DDA", trim_imp_start, trim_imp_end, outdir+"/cSSTF_"+str(angle)+"_"+LR+".DDB")
    # ######################################################################


def mic_ajust():
    playrec_2ch(5, "/tmp/rec.DSB")
    speach(2, "/tmp/rec.DSB")
    averaging("/tmp/rec_1.DSB", 5, "/tmp/rec_L.DDB")
    averaging("/tmp/rec_2.DSB", 5, "/tmp/rec_R.DDB")
