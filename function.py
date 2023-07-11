import os
import sys
from PyQt5.Qt import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import webbrowser
import json


launchSet={}

def warn():
        msg_box = QMessageBox()
        msg_box.setFont(QtGui.QFont('Microsoft YaHei', 18))
        msg_box.setWindowTitle('提示') 
        msg_box.setText('  未能检测到models文件夹！\n  请将启动程序放在tgwebui根目录下！')
        msg_box.exec_() 

def getDirSize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return size

# def getNvidia():

#     if torch.cuda.is_available():
#         device = torch.cuda.get_device_name(0)
#         total_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3  # 显存以GB为单位
#         print(f"GPU型号：{device}")
#         print(f"总显存：{total_memory} GB")
#     else:
#         print("没有可用的GPU设备。")



def fixBitsandbytes():

    file_path = r'conda\Lib\site-packages\bitsandbytes\cuda_setup\main.py'
    search_line = "if not torch.cuda.is_available(): return 'libbitsandbytes_cpu'+SHARED_LIB_EXTENSION, None, None, None, None"
    replace_line = "    if torch.cuda.is_available(): return 'libbitsandbytes_cuda117.dll', None, None, None, None"

    # 读取文件内容
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 寻找并替换指定内容
    for i, line in enumerate(lines):
        if line.strip() == search_line:
            lines[i] = replace_line + '\n'
            break

    # 将修改后的内容写入文件
    with open(file_path, 'w') as file:
        file.writelines(lines)

def changeAGNAPI():

    file_path = r'tools\agnai\srv\adapter\openai.ts'
    search_line = "const baseUrl = `https://api.openai.com`"
    replace_line = "const baseUrl = `https://r.cydrvp.top/proxy/api.openai.com`"

    try:

        with open(file_path, 'r',encoding="utf-8") as file:
            lines = file.readlines()


        for i, line in enumerate(lines):
            if line.strip() == search_line:
                lines[i] = replace_line + '\n'
                break


        with open(file_path, 'w',encoding="utf-8") as file:
            file.writelines(lines)  

    except FileNotFoundError:
        print()

def changeTAAPI():

    file_path = r'tools\SillyTavern\server.js'
    search_line = """let api_openai = "https://api.openai.com/v1";"""
    replace_line = """let api_openai = "https://r.cydrvp.top/proxy/api.openai.com/v1";"""

    try:

        with open(file_path, 'r',encoding="utf-8") as file:
            lines = file.readlines()


        for i, line in enumerate(lines):
            if line.strip() == search_line:
                lines[i] = replace_line + '\n'
                break


        with open(file_path, 'w',encoding="utf-8") as file:
            file.writelines(lines)  

    except FileNotFoundError:
        print()

def getLaunchSet(ui):
    global launchSet
    launchInput="--auto-launch "
    launchSet= {
        'hoChose':ui.hoChose.currentText(),
        'laMode':ui.laMode.currentText(),
        'laApi':ui.laApi.isChecked(),
        'laOpt':ui.laOpt.text(),
        'laRunMode':ui.laRunMode.currentText(),
        'laTru':ui.laTru.isChecked(),
        'laGptqW':ui.laGptqW.currentText(),
        'laGptqGro':ui.laGptqGro.currentText(),
        'laGptqType':ui.laGptqType.currentText(),
        'laPre':ui.laPre.text(),
        'laAuto':ui.laAuto.isChecked(),
        'laEnviro':ui.laEnviro.currentText(),
        'laGPTQWay':ui.laGPTQWay.currentText(),
        'laBits':ui.laBits.currentText(),
        'upGit':ui.upGit.currentText(),
        'laMonkey':ui.laMonkey.isChecked(),
        'laRWKVStrategy':ui.laRWKVStrategy.currentText(),
        'laRWKVCUDA':ui.laRWKVCUDA.isChecked(),
        'laloadway':ui.laloadway.currentText(),
        'laGGMLlayer':ui.laGGMLlayer.text(),
        'laMaxTokens':ui.laMaxTokens.currentText(),
        'laModelDir':ui.laModelDir.text()
    }
    
    for key, value in launchSet.items():
        if key=="hoChose" and value!="":
            launchInput+="--model {} ".format(value)  
        if key=="laMode" and value=="Chat":
            launchInput+="--chat "
        if key=="laRunMode" and value=="CPU":
            launchInput+="--cpu "
        if key=="laApi" and value==True:
            launchInput+="--api "
        if key=="laTru" and value==True:
            launchInput+="--trust-remote-code "
        if key=="laOpt" and value!="":
            launchInput+=f"{launchSet['laOpt']} "
        if key=="laAuto" and value==True:
            launchInput+="--auto-devices "
        if key=="laGPTQWay" and value=="GPTQ-for-LLaMa":
            launchInput+="--loader gptq-for-llama "
            for key1, value1 in launchSet.items():
                if key1=="laGptqW" and value1!="":
                    launchInput+="--wbits {} ".format(value1)
                if key1=="laGptqGro" and value1!="":
                    launchInput+="--groupsize {} ".format(value1)
                if key1=="laGptqType" and value1!="":
                    launchInput+="--model_type {} ".format(value1)    
                if key1=="laPre" and value1!="":
                    launchInput+="--pre_layer {} ".format(value1) 
        if key=="laGPTQWay" and value=="AutoGPTQ":
            launchInput+="--loader autogptq "
        if key=="laGPTQWay" and value=="ExLlama":
            launchInput+="--loader exllama "
        if key=="laGPTQWay" and value=="ExLlama_HF":
            launchInput+="--loader exllama_hf "
        if key=="laloadway" and value=="transformers":
            launchInput+="--loader transformers "
        if key=="laloadway" and value=="llamacpp":
            launchInput+="--loader llamacpp "
        if key=="laloadway" and value=="rwkv":
            launchInput+="--loader rwkv "
        if key=="laBits" and value=="8bit精度":
            launchInput+="--load-in-8bit "   
        if key=="laBits" and value=="4bit精度":
            launchInput+="--load-in-4bit "  
        if key=="laMonkey" and value==True:
            launchInput+="--monkey-patch "  
        if key=="laRWKVCUDA" and value==True:
            launchInput+="--rwkv-cuda-on "
        if key=="laRWKVStrategy" and value!="":
            launchInput+="--rwkv-strategy {} ".format(value) 
        if key=="laGGMLlayer" and value!="":
            launchInput+="--n-gpu-layers {} ".format(value) 
        if key=="laMaxTokens" and value!="":
            if value=="2048tokens（2048+1）":
                launchInput+="--max_seq_len 2048  --compress_pos_emb 1 "
            elif value=="4096tokens（4096+2）":
                launchInput+="--max_seq_len 4096  --compress_pos_emb 2 "
            elif value=="6144tokens（6144+3）":
                launchInput+="--max_seq_len 6144  --compress_pos_emb 3 "
            elif value=="8192tokens（8192+4）":
                launchInput+="--max_seq_len 8192  --compress_pos_emb 4 "
        if key=="laModelDir" and value!="":
            launchInput+=f"--model-dir {launchSet['laModelDir']} "
    return launchInput
                   
def saveLaunchSet():
    with open('launchSetting.json', 'w') as f:
        json.dump(launchSet, f)

def getDownload(ui):
    downloadName=ui.moHugg.text()
    return downloadName

def downloadBat(ui):
    downloadName=getDownload(ui)
    if ui.moText.isChecked()==True:
        bat_content = """
        @echo off
        chcp 65001
        pushd %~dp0
        cd conda
        call .\\Scripts\\activate.bat
        cd ..
        echo.
        echo 当前下载模型名称是(仅下载配置文件): {}
        echo.
        python download-model.py --text-only {} 
        echo.
        echo ----------------------------------------------------------------------------------------------------
        echo 下载模型环节结束！若出现 "requests.exceptions.HTTPError: 401 Client Error: Unauthorized for url:"等字样，说明您输入的内容无法在hugging face上找到，下载失败。
        pause
        """.format(downloadName,downloadName)
    else:
        bat_content = """
        @echo off
        chcp 65001
        pushd %~dp0
        cd conda
        call .\\Scripts\\activate.bat
        cd ..
        echo 当前下载模型名称是: {}
        echo.
        python download-model.py {} 
        echo.
        echo ----------------------------------------------------------------------------------------------------
        echo 下载模型环节结束！若出现 "requests.exceptions.HTTPError: 401 Client Error: Unauthorized for url:"等字样，说明您输入的内容无法在hugging face上找到，下载失败。
        pause
        """.format(downloadName,downloadName)

    bat_file = "downloadModel.bat"
    with open(bat_file, "w",encoding="utf-8") as f:
        f.write(bat_content)
    os.system('.\\downloadModel.bat')
    os.remove('.\\downloadModel.bat') 
def updateBat(ui):
    if ui.upGit.currentText()=="Github":
        bat_content = """
        @echo off
        chcp 65001
        pushd %~dp0
        cd conda
        call .\\Scripts\\activate.bat
        cd ..
        git remote set-url origin https://github.com/oobabooga/text-generation-webui/
        echo.
        echo 当前使用Github源更新: 
        echo.
        git stash push -m "requirements.txt" requirements.txt
        echo.
        git stash clear
        git pull
        echo.
        echo ----------------------------------------------------------------------------------------------------
        echo 更新结束。
        echo.
        echo 若提示 files changed, xx insertions(+), yy deletions(-)，且上方出现红绿色加号+，则代表更新成功。
        echo.
        echo 若提示 Already up to date.则代表已经是最新版了，无需更新。
        echo.
        echo 若提示 fatal: unable to access xxx: Recv failure: Connection was reset 则说明连接失败，请尝试使用KGithub源更新。
        pause
        """
    else:
        bat_content = """
        @echo off
        chcp 65001
        pushd %~dp0
        cd conda
        call .\\Scripts\\activate.bat
        cd ..
        git remote set-url origin https://kgithub.com/oobabooga/text-generation-webui/
        echo.
        echo 当前使用KGithub镜像源更新: 
        echo.
        git stash push -m "requirements.txt" requirements.txt
        echo.
        git stash clear
        git pull
        echo.
        echo ----------------------------------------------------------------------------------------------------
        echo 更新结束。
        echo.
        echo 若提示 files changed, xx insertions(+), yy deletions(-)，且上方出现红绿色加号+，则代表更新成功。
        echo.
        echo 若提示 Already up to date.则代表已经是最新版了，无需更新。
        echo.
        echo 若提示 fatal: unable to access xxx: Recv failure: Connection was reset 则说明连接失败，请尝试使用KGithub源更新。
        pause
        """
    bat_file = "update.bat"
    with open(bat_file, "w",encoding="utf-8") as f:
        f.write(bat_content)
    os.system('.\\update.bat')
    os.remove('.\\update.bat')
def runBat(ui):
    launchInput=getLaunchSet(ui)
    saveLaunchSet()
    bat_content=None
####################################################
    bat_content_lrb = """
    @echo off
    chcp 65001
    pushd %~dp0
    cd conda
    call .\\Scripts\\activate.bat
    cd ..
    echo.
    echo 使用懒人包环境 当前启动参数是: {}
    python server.py {}
    echo.
    echo webui已关闭！若浏览器没有自动打开webui网页而直接关闭的话，说明启动出现异常。
    pause
    """.format(launchInput,launchInput)
####################################################
    bat_content_user = """
    @echo off
    chcp 65001
    echo.
    echo 使用本机环境 当前启动参数是: {}
    python server.py {}
    echo.
    echo webui已关闭！若浏览器没有自动打开webui网页而直接关闭的话，说明启动出现异常。
    pause
    """.format(launchInput,launchInput)
####################################################
    bat_content_conda = """
    @echo off
    chcp 65001
    pushd %~dp0
    cd ..
    set CONDA_ROOT_PREFIX=%cd%\installer_files\conda
    set INSTALL_ENV_DIR=%cd%\installer_files\env
    call "%CONDA_ROOT_PREFIX%\condabin\conda.bat" activate "%INSTALL_ENV_DIR%" 
    cd text-generation-webui
    echo.
    echo 使用Conda环境(One-click installers) 当前启动参数是: {}
    python server.py {}
    echo.
    echo webui已关闭！若浏览器没有自动打开webui网页而直接关闭的话，说明启动出现异常。
    pause
    """.format(launchInput,launchInput)
####################################################
    # bat_content_virtualenv = """
    # @echo off
    # env\\Scripts\\activate
    # echo.
    # echo 使用virtualenv环境 当前启动参数是: {}
    # python server.py {}
    # echo.
    # echo webui已关闭！若浏览器没有自动打开webui网页而直接关闭的话，说明启动出现异常。
    # pause
    # """.format(launchInput,launchInput)
####################################################
    if launchSet['laEnviro']=="懒人包环境":
         bat_content=bat_content_lrb
    elif launchSet['laEnviro']=="本机环境":
         bat_content=bat_content_user
    elif  launchSet['laEnviro']=="Conda环境(One-click installers)":
         bat_content=bat_content_conda
    # elif  launchSet['laEnviro']=="virtualenv环境":
    #      bat_content=bat_content_virtualenv

    bat_file = "runTgwebui.bat"
    with open(bat_file, "w",encoding="utf-8") as f:
        f.write(bat_content)
    os.system('.\\runTgwebui.bat')

def updateRequirementsBat():
    bat_content= """
    @echo off
    chcp 65001
    pushd %~dp0
    cd conda
    call .\\Scripts\\activate.bat
    cd ..
    echo.
    echo 更新懒人包环境依赖中
    pip install -r requirements.txt
    echo.
    echo 更新结束。请仔细观察输出日志是否有ERROR提示。
    pause
    """
    bat_file = "updateRequirements.bat"
    with open(bat_file, "w",encoding="utf-8") as f:
        f.write(bat_content)
    os.system('.\\updateRequirements.bat')
    fixBitsandbytes()
    os.remove('.\\updateRequirements.bat')

def versionFallbackBat():

    bat_content= """
    @echo off
    chcp 65001
    pushd %~dp0
    cd conda
    call .\\Scripts\\activate.bat
    cd ..
    echo.
    set OUTPUT_FILE=commits.txt
    git log > %OUTPUT_FILE%
    """
    bat_file = "getCommit.bat"
    with open(bat_file, "w",encoding="utf-8") as f:
        f.write(bat_content)
    os.system('.\\getCommit.bat')
    os.remove('.\\getCommit.bat') 

    commit_list = []

    with open("commits.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("commit "):
                commit = line.replace("commit ", "")
                commit_list.append(commit)
 
    bat_content= """
    @echo off
    chcp 65001
    pushd %~dp0
    cd conda
    call .\\Scripts\\activate.bat
    cd ..
    echo.
    echo text-generation-webui版本回退中
    git reset --hard {}
    echo.
    echo 版本回退结束
    pause
    """.format(commit_list[1])
    bat_file = "versionFallback.bat"
    with open(bat_file, "w",encoding="utf-8") as f:
        f.write(bat_content)
    os.system('.\\versionFallback.bat')
    os.remove('.\\versionFallback.bat')
def readLaunchSetFromJson(ui):
        try:
                with open(".\\launchSetting.json", 'r') as f:
                        launchSet = json.load(f)

                if launchSet.get('hoChose')!=None and launchSet.get('hoChose')!="":
                    ui.hoChose.setCurrentText(launchSet['hoChose'])

                if launchSet.get('laMode')!=None and launchSet.get('laMode')!="":
                    ui.laMode.setCurrentText(launchSet['laMode'])
                
                if launchSet.get('laRunMode')!=None and launchSet.get('laRunMode')!="":
                    ui.laRunMode.setCurrentText(launchSet['laRunMode'])
                
                if launchSet.get('laGptqW')!=None and launchSet.get('laGptqW')!="":
                    ui.laGptqW.setCurrentText(launchSet['laGptqW'])

                if launchSet.get('laGptqGro')!=None and launchSet.get('laGptqGro')!="":
                    ui.laGptqGro.setCurrentText(launchSet['laGptqGro'])

                if launchSet.get('laGptqType')!=None and launchSet.get('laGptqType')!="":
                    ui.laGptqType.setCurrentText(launchSet['laGptqType'])

                if launchSet.get('upGit')!=None and launchSet.get('upGit')!="":
                    ui.upGit.setCurrentText(launchSet['upGit'])

                if launchSet.get('laApi')!=None and launchSet.get('laApi')!="":
                    ui.laApi.setChecked(launchSet.get('laApi'))

                if launchSet.get('laOpt')!=None and launchSet.get('laOpt')!="":
                    ui.laOpt.setText(launchSet.get('laOpt'))
                
                if launchSet.get('laTru')!=None and launchSet.get('laTru')!="":
                    ui.laTru.setChecked(launchSet.get('laTru'))
                
                if launchSet.get('laPre')!=None and launchSet.get('laPre')!="":
                    ui.laPre.setText(launchSet.get('laPre'))
                
                if launchSet.get('laAuto')!=None and launchSet.get('laAuto')!="":
                    ui.laAuto.setChecked(launchSet.get('laAuto'))
                
                if launchSet.get('laEnviro')!=None and launchSet.get('laEnviro')!="":
                    ui.laEnviro.setCurrentText(launchSet['laEnviro'])

                if launchSet.get('laGPTQWay')!=None and launchSet.get('laGPTQWay')!="":
                    ui.laGPTQWay.setCurrentText(launchSet['laGPTQWay'])

                if launchSet.get('laBits')!=None and launchSet.get('laBits')!="":
                    ui.laBits.setCurrentText(launchSet['laBits'])

                if launchSet.get('laMonkey')!=None and launchSet.get('laMonkey')!="":
                    ui.laMonkey.setChecked(launchSet.get('laMonkey'))

                if launchSet.get('laRWKVCUDA')!=None and launchSet.get('laRWKVCUDA')!="":
                    ui.laRWKVCUDA.setChecked(launchSet.get('laRWKVCUDA'))

                if launchSet.get('laRWKVStrategy')!=None and launchSet.get('laRWKVStrategy')!="":
                    ui.laRWKVStrategy.setCurrentText(launchSet['laRWKVStrategy'])
                
                if launchSet.get('laGGMLlayer')!=None and launchSet.get('laGGMLlayer')!="":
                    ui.laGGMLlayer.setText(launchSet.get('laGGMLlayer'))

                if launchSet.get('laloadway')!=None and launchSet.get('laloadway')!="":
                    ui.laloadway.setCurrentText(launchSet['laloadway'])

                if launchSet.get('laMaxTokens')!=None and launchSet.get('laMaxTokens')!="":
                    ui.laMaxTokens.setCurrentText(launchSet['laMaxTokens'])

                if launchSet.get('laModelDir')!=None and launchSet.get('laModelDir')!="":
                    ui.laModelDir.setText(launchSet.get('laModelDir'))
                
        except FileNotFoundError:
                return

def updateModelList(ui):
    no=0
    _translate = QtCore.QCoreApplication.translate
    folder_path = ".\\models"
    try:
        ui.hoChose.clear()
        ui.moList.clear()
        model = [folder for folder in os.listdir(folder_path)
        if folder not in ['place-your-models-here.txt', 'config.yaml','20B_tokenizer.json']]
        for ele in model: 
                ui.hoChose.addItem(ele)
                file_path = os.path.join(folder_path, ele)
                if os.path.isdir(file_path):#统计文件夹大小
                        newmodellist = QtWidgets.QTreeWidgetItem(ui.moList)
                        file_size = getDirSize(file_path)
                        file_size=file_size / (1024 * 1024 * 1024)
                        ui.moList.topLevelItem(no).setText(0, _translate("Form",str(no+1)))
                        ui.moList.topLevelItem(no).setText(1, _translate("Form",f"{file_size:.2f} GB"))
                        ui.moList.topLevelItem(no).setText(2, _translate("Form",ele))
                elif os.path.isfile(file_path):#统计文件大小
                        newmodellist = QtWidgets.QTreeWidgetItem(ui.moList)
                        file_size = os.path.getsize(file_path)
                        file_size=file_size / (1024 * 1024 * 1024)
                        ui.moList.topLevelItem(no).setText(0, _translate("Form",str(no+1)))
                        ui.moList.topLevelItem(no).setText(1, _translate("Form",f"{file_size:.2f} GB"))
                        ui.moList.topLevelItem(no).setText(2, _translate("Form",ele))
                no+=1
    except FileNotFoundError:
        warn()
        sys.exit()

def openAgnai():
    bat_content= """
    @echo off
    chcp 65001
    pushd %~dp0
    cd conda
    call .\\Scripts\\activate.bat
    cd ..
    echo.
    cd tools\\agnai
    echo agn-ai开启中 启动成功后请在 http://127.0.0.1:3001/ 打开
    echo.
    call node srv/bin.js
    echo.
    echo agn-ai运行结束
    pause
    """
    bat_file = "runAgnai.bat"
    with open(bat_file, "w",encoding="utf-8") as f:
        f.write(bat_content)
    os.system('.\\runAgnai.bat')
    os.remove('.\\runAgnai.bat')
def updateAgnai(ui):
    bat_content_github= """
    @echo off
    chcp 65001
    pushd %~dp0
    cd conda
    call .\\Scripts\\activate.bat
    cd ..
    echo.
    cd tools\\agnai
    echo agn-ai更新中
    echo.
    git remote set-url origin https://github.com/agnaistic/agnai/
    echo.
    echo 当前使用Github源更新: 
    git stash push -m "openai.ts" srv\\adapter\\openai.ts
    echo.
    git stash clear
    git pull
    echo.
    pause
    """

    bat_content_Kgithub= """
    @echo off
    chcp 65001
    pushd %~dp0
    cd conda
    call .\\Scripts\\activate.bat
    cd ..
    echo.
    cd tools\\agnai
    echo agn-ai更新中
    echo.
    git remote set-url origin https://kgithub.com/agnaistic/agnai/
    echo.
    echo 当前使用KGithub源更新: 
    git stash push -m "openai.ts" srv\\adapter\\openai.ts
    echo.
    git stash clear
    git pull
    echo.
    pause
    """

    if ui.toAgnGit.currentText()=="Github":
        bat_content=bat_content_github
    else:
        bat_content=bat_content_Kgithub
        
    bat_file = "updateAgnai1.bat"
    with open(bat_file, "w",encoding="utf-8") as f:
        f.write(bat_content)
    os.system('.\\updateAgnai1.bat')
    os.remove('.\\updateAgnai1.bat')
    changeAGNAPI()

    bat_content= """
    @echo off
    chcp 65001
    pushd %~dp0
    cd conda
    call .\\Scripts\\activate.bat
    cd ..
    echo.
    cd tools\\agnai
    echo.
    call npm run deps
    echo.
    call npm run build:all
    echo.
    echo agn-ai更新结束
    pause
    """
    bat_file = "updateAgnai2.bat"
    with open(bat_file, "w",encoding="utf-8") as f:
        f.write(bat_content)
    os.system('.\\updateAgnai2.bat')
    os.remove('.\\updateAgnai2.bat')

def openTav():
    bat_content= """
    @echo off
    chcp 65001
    pushd %~dp0
    cd conda
    call .\\Scripts\\activate.bat
    cd ..
    echo.
    cd tools\\SillyTavern
    echo SillyTavern开启中 启动成功后请在 http://127.0.0.1:8000/ 打开
    echo.
    call node server.js
    echo SillyTavern运行结束
    pause
    """
    bat_file = "runSillyTavern.bat"
    with open(bat_file, "w",encoding="utf-8") as f:
        f.write(bat_content)
    os.system('.\\runSillyTavern.bat')
    os.remove('.\\runSillyTavern.bat')
def updateTAai(ui):
    bat_content_github= """
    @echo off
    chcp 65001
    pushd %~dp0
    cd conda
    call .\\Scripts\\activate.bat
    cd ..
    echo.
    cd tools\\SillyTavern
    echo SillyTavern更新中
    echo.
    git remote set-url origin https://github.com/SillyTavern/SillyTavern
    echo.
    echo 当前使用Github源更新: 
    echo.
    git stash push -m "server.js" server.js
    echo.
    git stash clear
    git pull
    echo.
    pause
    """

    bat_content_Kgithub= """
    @echo off
    chcp 65001
    pushd %~dp0
    cd conda
    call .\\Scripts\\activate.bat
    cd ..
    echo.
    cd tools\\SillyTavern
    echo SillyTavern更新中
    echo.
    git remote set-url origin https://kgithub.com/SillyTavern/SillyTavern
    echo.
    echo 当前使用KGithub源更新: 
    echo.
    git stash push -m "server.js" server.js
    echo.
    git stash clear
    git pull
    echo.
    pause
    """

    if ui.toTaGit.currentText()=="Github":
        bat_content=bat_content_github
    else:
        bat_content=bat_content_Kgithub
        
    bat_file = "updateTAV1.bat"
    with open(bat_file, "w",encoding="utf-8") as f:
        f.write(bat_content)
    os.system('.\\updateTAV1.bat')
    os.remove('.\\updateTAV1.bat')
    changeTAAPI()

    bat_content= """
    @echo off
    chcp 65001
    pushd %~dp0
    cd conda
    call .\\Scripts\\activate.bat
    cd ..
    echo.
    cd tools\\SillyTavern
    echo.
    call npm install
    echo.
    echo SillyTavern更新结束
    pause
    """
    bat_file = "updateTAV2.bat"
    with open(bat_file, "w",encoding="utf-8") as f:
        f.write(bat_content)
    os.system('.\\updateTAV2.bat')
    os.remove('.\\updateTAV2.bat')

def openEnv():
    bat_content= """
    @echo off
    chcp 65001
    pushd %~dp0
    cd conda
    call .\\Scripts\\activate.bat
    cd ..
    start cmd
    """
    bat_file = "openEnv.bat"
    with open(bat_file, "w",encoding="utf-8") as f:
        f.write(bat_content)
    os.system('.\\openEnv.bat')
    os.remove('.\\openEnv.bat')
def openBilibili():
    url="https://space.bilibili.com/283750111"
    webbrowser.open(url)

def openGithub():
    url="https://github.com/oobabooga/text-generation-webui"
    webbrowser.open(url)

def openMakeCharaCard():
    url="https://zoltanai.github.io/character-editor/"
    webbrowser.open(url)

def openCharaHub():
    url="https://www.characterhub.org/characters"
    webbrowser.open(url)

def openCai():
    url="https://beta.character.ai/"
    webbrowser.open(url)

def openWr():
    url="https://www.bilibili.com/read/cv23877210/"
    webbrowser.open(url)

def openPyg():
    url="https://discord.com/invite/pygmalionai/"
    webbrowser.open(url)

def getAnnoucement(ui):
    url = 'https://gitee.com/teyasi/lazy-person-package-tgwebui/raw/master/announcement.txt'
    try:
        content = requests.get(url)
        content.encoding = 'utf-8'
        ui.hoAnno.setPlainText(content.text)
    except requests.exceptions.RequestException as e:
        return

def ggmlGPU():
    bat_content= """
    @echo off
    chcp 65001
    pushd %~dp0
    cd conda
    call .\\Scripts\\activate.bat
    cd ..
    echo.
    echo 编译加速开始
    pip uninstall -y llama-cpp-python
    set CMAKE_ARGS="-DLLAMA_CUBLAS=on"
    set FORCE_CMAKE=1
    pip install llama-cpp-python --no-cache-dir
    echo 编译加速结束。请仔细观察输出日志是否有ERROR提示。
    pause
    """
    bat_file = "ggmlGPU.bat"
    with open(bat_file, "w",encoding="utf-8") as f:
        f.write(bat_content)
    os.system('.\\ggmlGPU.bat')
    os.remove('.\\ggmlGPU.bat')