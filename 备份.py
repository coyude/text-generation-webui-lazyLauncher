from function import *
#############################################################自定义线程begin
UI=None

class laThread(QThread): #启动线程
    _signal =pyqtSignal()
    def __init__(self):
        super().__init__()
    def run(self):
        global UI
        runBat(UI)
        self._signal.emit()

class doThread(QThread): #下载模型线程
    _signal =pyqtSignal()
    def __init__(self):
        super().__init__()
    def run(self):
        global UI
        downloadBat(UI)
        self._signal.emit()

class upThread(QThread): #更新tgwebui线程
    _signal =pyqtSignal()
    def __init__(self):
        super().__init__()
    def run(self):
        global UI
        updateBat(UI)
        self._signal.emit()

class faThread(QThread): #版本回退线程
    _signal =pyqtSignal()
    def __init__(self):
        super().__init__()
    def run(self):
        global UI
        versionFallbackBat()
        self._signal.emit()

class inThread(QThread): #更新依赖线程
    _signal =pyqtSignal()
    def __init__(self):
        super().__init__()
    def run(self):
        global UI
        updateRequirementsBat()
        self._signal.emit()

class agnRunThread(QThread): #agn-ai运行线程
    _signal =pyqtSignal()
    def __init__(self):
        super().__init__()
    def run(self):
        global UI
        openAgnai()
        self._signal.emit()

class agnUpdateThread(QThread): #agn-ai更新线程
    _signal =pyqtSignal()
    def __init__(self):
        super().__init__()
    def run(self):
        global UI
        updateAgnai(UI)
        self._signal.emit()

class tavRunThread(QThread): #sillytavernai运行线程
    _signal =pyqtSignal()
    def __init__(self):
        super().__init__()
    def run(self):
        global UI
        openTav()
        self._signal.emit()

class tavUpdateThread(QThread): #sillytavernai更新线程
    _signal =pyqtSignal()
    def __init__(self):
        super().__init__()
    def run(self):
        global UI
        updateTAai(UI)
        self._signal.emit()

class ggmlGPUThread(QThread): #ggml启用GPU加速线程
    _signal =pyqtSignal()
    def __init__(self):
        super().__init__()
    def run(self):
        global UI
        ggmlGPU()
        self._signal.emit()      
# #############################################################自定义线程end














###############################################################自定义模块和信号与槽函数begin

        getAnnoucement(self) #获取公告
        updateModelList(self) #更新可加载模型的选项
        #如果启动器设置launchSetting.json存在的话
        readLaunchSetFromJson(self) #从文件读取启动器设置
        #若launchSetting.json不存在的话
        getLaunchSet(self) #获取当前启动器设置
        saveLaunchSet() #保存启动器设置到launchSetting.json
        
        self.hoRefresh.clicked.connect(lambda:updateModelList(self))
        self.moRefresh.clicked.connect(lambda:updateModelList(self))
        self.hoRun.clicked.connect(self.launchCh) 
        self.moStart.clicked.connect(self.downloadCh)
        self.upStart.clicked.connect(self.updateCh)
        self.upBack.clicked.connect(self.fallbackCh)
        self.upInstall.clicked.connect(self.installReCh)
        self.more_bili.clicked.connect(openBilibili)
        self.more_tgwebui.clicked.connect(openGithub)
        self.toWr.clicked.connect(openWr)
        self.toChar.clicked.connect(openCharaHub)
        self.toCAI.clicked.connect(openCai)
        self.toPyg.clicked.connect(openPyg)
        self.toCE.clicked.connect(openMakeCharaCard)
        self.toAgnRun.clicked.connect(self.opAgnaiCh)
        self.toAgnUp.clicked.connect(self.upAgnaiCh)
        self.toTaRu.clicked.connect(self.opTavCh)
        self.toTaUp.clicked.connect(self.upTavCh)
        self.upOpen.clicked.connect(openEnv)
        self.laGGMLGPUON.clicked.connect(self.ggmlCh)

    def launchCh(self):#启动
        global UI
        UI=ui
        self.hoRun.setEnabled(False)
        self.runThread = laThread()
        self.runThread._signal.connect(self.hoRun_btn)
        self.runThread.start()

    def downloadCh(self):#下载模型
        global UI
        UI=ui
        self.moStart.setEnabled(False)
        self.downThread = doThread()
        self.downThread._signal.connect(self.moStart_btn)
        self.downThread.start()

    def updateCh(self):#更新tgwebui
        global UI
        UI=ui
        self.upStart.setEnabled(False)
        self.updateThread = upThread()
        self.updateThread._signal.connect(self.upStart_btn)
        self.updateThread.start()

    def fallbackCh(self):#版本回退
        global UI
        UI=ui
        self.upBack.setEnabled(False)
        self.fallbackthread = faThread()
        self.fallbackthread._signal.connect(self.fallback_btn)
        self.fallbackthread.start()

    def installReCh(self):#更新依赖
        global UI
        UI=ui
        self.upInstall.setEnabled(False)
        self.upInstallthread = inThread()
        self.upInstallthread._signal.connect(self.upRe_btn)
        self.upInstallthread.start()

    def opAgnaiCh(self):#打开agn-ai
        global UI
        UI=ui
        self.toAgnRun.setEnabled(False)
        self.toagnRunThread = agnRunThread()
        self.toagnRunThread._signal.connect(self.toAgnRun_btn)
        self.toagnRunThread.start()

    def upAgnaiCh(self):#更新agn-ai
        global UI
        UI=ui
        self.toAgnUp.setEnabled(False)
        self.toagnUpdateThread = agnUpdateThread()
        self.toagnUpdateThread._signal.connect(self.toAgnUp_btn)
        self.toagnUpdateThread.start()

    def opTavCh(self):#打开SillyTavern
        global UI
        UI=ui
        self.toTaRu.setEnabled(False)
        self.totavRunThread = tavRunThread()
        self.totavRunThread._signal.connect(self.toTARun_btn)
        self.totavRunThread.start()

    def upTavCh(self):#更新SillyTavern
        global UI
        UI=ui
        self.toTaUp.setEnabled(False)
        self.totavUpdateThread = tavUpdateThread()
        self.totavUpdateThread._signal.connect(self.toTAUp_btn)
        self.totavUpdateThread.start()

    def ggmlCh(self):#启动ggml的GPU加速
        global UI
        UI=ui
        self.laGGMLGPUON.setEnabled(False)
        self.ggmlGPUThread = ggmlGPUThread()
        self.ggmlGPUThread._signal.connect(self.laGGMLbtn)
        self.ggmlGPUThread.start()




    def hoRun_btn(self):
        self.hoRun.setEnabled(True)
    def moStart_btn(self):
        self.moStart.setEnabled(True)
    def upStart_btn(self):
        self.upStart.setEnabled(True)
    def fallback_btn(self):
        self.upBack.setEnabled(True)
    def upRe_btn(self):
        self.upInstall.setEnabled(True)
    def toTARun_btn(self):
        self.toTaRu.setEnabled(True)
    def toTAUp_btn(self):
        self.toTaUp.setEnabled(True)
    def toAgnRun_btn(self):
        self.toAgnRun.setEnabled(True)
    def toAgnUp_btn(self):
        self.toAgnUp.setEnabled(True)
    def laGGMLbtn(self):
        self.laGGMLGPUON.setEnabled(True)


# # ##############################################################自定义模块end
import s_rc
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
