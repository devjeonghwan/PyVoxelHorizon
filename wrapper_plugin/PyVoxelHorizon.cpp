#include "pch.h"
#include "PyVoxelHorizon.h"


PyObject* PyObject_GetAttrStringIfExists(PyObject* pPyObject, const char* szName) {
    if (!PyObject_HasAttrString(pPyObject, szName)) {
        return NULL;
    }

    return PyObject_GetAttrString(pPyObject, szName);
}


PyVoxelHorizon::PyVoxelHorizon()
{
#ifdef _DEBUG
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif

    this->m_IsPythonInitialized = false;

    this->m_pPythonGameHook = NULL;

    this->m_pPythonOnStartScene = NULL;
    this->m_pPythonOnRun = NULL;
    this->m_pPythonOnDestroyScene = NULL;

    this->m_pPythonOnMouseLButtonDown = NULL;
    this->m_pPythonOnMouseLButtonUp = NULL;
    this->m_pPythonOnMouseRButtonDown = NULL;
    this->m_pPythonOnMouseRButtonUp = NULL;
    this->m_pPythonOnMouseMove = NULL;
    this->m_pPythonOnMouseMoveHV = NULL;
    this->m_pPythonOnMouseWheel = NULL;

    this->m_pPythonOnKeyDown = NULL;
    this->m_pPythonOnKeyUp = NULL;
    this->m_pPythonOnCharUnicode = NULL;

    this->m_pPythonOnDPadLB = NULL;
    this->m_pPythonOffDPadLB = NULL;
    this->m_pPythonOnDPadRB = NULL;
    this->m_pPythonOffDPadRB = NULL;

    this->m_pPythonOnDPadUp = NULL;
    this->m_pPythonOnDPadDown = NULL;
    this->m_pPythonOnDPadLeft = NULL;
    this->m_pPythonOnDPadRight = NULL;
    this->m_pPythonOffDPadUp = NULL;
    this->m_pPythonOffDPadDown = NULL;
    this->m_pPythonOffDPadLeft = NULL;
    this->m_pPythonOffDPadRight = NULL;

    this->m_pPythonOnPadPressedA = NULL;
    this->m_pPythonOnPadPressedB = NULL;
    this->m_pPythonOnPadPressedX = NULL;
    this->m_pPythonOnPadPressedY = NULL;
    this->m_pPythonOffPadPressedA = NULL;
    this->m_pPythonOffPadPressedB = NULL;
    this->m_pPythonOffPadPressedX = NULL;
    this->m_pPythonOffPadPressedY = NULL;

    this->m_pPythonOnKeyDownFunc = NULL;
    this->m_pPythonOnKeyDownCtrlFunc = NULL;

    this->m_pPythonOnPreConsoleCommand = NULL;
}

PyVoxelHorizon::~PyVoxelHorizon()
{
    if (this->m_pPythonGameHook != NULL) {
        Py_DECREF(this->m_pPythonGameHook);
        this->m_pPythonGameHook = NULL;
    }

    if (this->m_pPythonOnStartScene != NULL) {
        Py_DECREF(this->m_pPythonOnStartScene);
        this->m_pPythonOnStartScene = NULL;
    }
    if (this->m_pPythonOnRun != NULL) {
        Py_DECREF(this->m_pPythonOnRun);
        this->m_pPythonOnRun = NULL;
    }
    if (this->m_pPythonOnDestroyScene != NULL) {
        Py_DECREF(this->m_pPythonOnDestroyScene);
        this->m_pPythonOnDestroyScene = NULL;
    }

    if (this->m_pPythonOnMouseLButtonDown != NULL) {
        Py_DECREF(this->m_pPythonOnMouseLButtonDown);
        this->m_pPythonOnMouseLButtonDown = NULL;
    }
    if (this->m_pPythonOnMouseLButtonUp != NULL) {
        Py_DECREF(this->m_pPythonOnMouseLButtonUp);
        this->m_pPythonOnMouseLButtonUp = NULL;
    }
    if (this->m_pPythonOnMouseRButtonDown != NULL) {
        Py_DECREF(this->m_pPythonOnMouseRButtonDown);
        this->m_pPythonOnMouseRButtonDown = NULL;
    }
    if (this->m_pPythonOnMouseRButtonUp != NULL) {
        Py_DECREF(this->m_pPythonOnMouseRButtonUp);
        this->m_pPythonOnMouseRButtonUp = NULL;
    }
    if (this->m_pPythonOnMouseMove != NULL) {
        Py_DECREF(this->m_pPythonOnMouseMove);
        this->m_pPythonOnMouseMove = NULL;
    }
    if (this->m_pPythonOnMouseMoveHV != NULL) {
        Py_DECREF(this->m_pPythonOnMouseMoveHV);
        this->m_pPythonOnMouseMoveHV = NULL;
    }
    if (this->m_pPythonOnMouseWheel != NULL) {
        Py_DECREF(this->m_pPythonOnMouseWheel);
        this->m_pPythonOnMouseWheel = NULL;
    }

    if (this->m_pPythonOnKeyDown != NULL) {
        Py_DECREF(this->m_pPythonOnKeyDown);
        this->m_pPythonOnKeyDown = NULL;
    }
    if (this->m_pPythonOnKeyUp != NULL) {
        Py_DECREF(this->m_pPythonOnKeyUp);
        this->m_pPythonOnKeyUp = NULL;
    }
    if (this->m_pPythonOnCharUnicode != NULL) {
        Py_DECREF(this->m_pPythonOnCharUnicode);
        this->m_pPythonOnCharUnicode = NULL;
    }

    if (this->m_pPythonOnDPadLB != NULL) {
        Py_DECREF(this->m_pPythonOnDPadLB);
        this->m_pPythonOnDPadLB = NULL;
    }
    if (this->m_pPythonOffDPadLB != NULL) {
        Py_DECREF(this->m_pPythonOffDPadLB);
        this->m_pPythonOffDPadLB = NULL;
    }
    if (this->m_pPythonOnDPadRB != NULL) {
        Py_DECREF(this->m_pPythonOnDPadRB);
        this->m_pPythonOnDPadRB = NULL;
    }
    if (this->m_pPythonOffDPadRB != NULL) {
        Py_DECREF(this->m_pPythonOffDPadRB);
        this->m_pPythonOffDPadRB = NULL;
    }

    if (this->m_pPythonOnDPadUp != NULL) {
        Py_DECREF(this->m_pPythonOnDPadUp);
        this->m_pPythonOnDPadUp = NULL;
    }
    if (this->m_pPythonOnDPadDown != NULL) {
        Py_DECREF(this->m_pPythonOnDPadDown);
        this->m_pPythonOnDPadDown = NULL;
    }
    if (this->m_pPythonOnDPadLeft != NULL) {
        Py_DECREF(this->m_pPythonOnDPadLeft);
        this->m_pPythonOnDPadLeft = NULL;
    }
    if (this->m_pPythonOnDPadRight != NULL) {
        Py_DECREF(this->m_pPythonOnDPadRight);
        this->m_pPythonOnDPadRight = NULL;
    }
    if (this->m_pPythonOffDPadUp != NULL) {
        Py_DECREF(this->m_pPythonOffDPadUp);
        this->m_pPythonOffDPadUp = NULL;
    }
    if (this->m_pPythonOffDPadDown != NULL) {
        Py_DECREF(this->m_pPythonOffDPadDown);
        this->m_pPythonOffDPadDown = NULL;
    }
    if (this->m_pPythonOffDPadLeft != NULL) {
        Py_DECREF(this->m_pPythonOffDPadLeft);
        this->m_pPythonOffDPadLeft = NULL;
    }
    if (this->m_pPythonOffDPadRight != NULL) {
        Py_DECREF(this->m_pPythonOffDPadRight);
        this->m_pPythonOffDPadRight = NULL;
    }

    if (this->m_pPythonOnPadPressedA != NULL) {
        Py_DECREF(this->m_pPythonOnPadPressedA);
        this->m_pPythonOnPadPressedA = NULL;
    }
    if (this->m_pPythonOnPadPressedB != NULL) {
        Py_DECREF(this->m_pPythonOnPadPressedB);
        this->m_pPythonOnPadPressedB = NULL;
    }
    if (this->m_pPythonOnPadPressedX != NULL) {
        Py_DECREF(this->m_pPythonOnPadPressedX);
        this->m_pPythonOnPadPressedX = NULL;
    }
    if (this->m_pPythonOnPadPressedY != NULL) {
        Py_DECREF(this->m_pPythonOnPadPressedY);
        this->m_pPythonOnPadPressedY = NULL;
    }
    if (this->m_pPythonOffPadPressedA != NULL) {
        Py_DECREF(this->m_pPythonOffPadPressedA);
        this->m_pPythonOffPadPressedA = NULL;
    }
    if (this->m_pPythonOffPadPressedB != NULL) {
        Py_DECREF(this->m_pPythonOffPadPressedB);
        this->m_pPythonOffPadPressedB = NULL;
    }
    if (this->m_pPythonOffPadPressedX != NULL) {
        Py_DECREF(this->m_pPythonOffPadPressedX);
        this->m_pPythonOffPadPressedX = NULL;
    }
    if (this->m_pPythonOffPadPressedY != NULL) {
        Py_DECREF(this->m_pPythonOffPadPressedY);
        this->m_pPythonOffPadPressedY = NULL;
    }

    if (this->m_pPythonOnKeyDownFunc != NULL) {
        Py_DECREF(this->m_pPythonOnKeyDownFunc);
        this->m_pPythonOnKeyDownFunc = NULL;
    }
    if (this->m_pPythonOnKeyDownCtrlFunc != NULL) {
        Py_DECREF(this->m_pPythonOnKeyDownCtrlFunc);
        this->m_pPythonOnKeyDownCtrlFunc = NULL;
    }

    if (this->m_pPythonOnPreConsoleCommand != NULL) {
        Py_DECREF(this->m_pPythonOnPreConsoleCommand);
        this->m_pPythonOnPreConsoleCommand = NULL;
    }

    if (this->m_pPythonOnMidiInput != NULL) {
        Py_DECREF(this->m_pPythonOnMidiInput);
        this->m_pPythonOnMidiInput = NULL;
    }
    if (this->m_pPythonOnMidiEventProcessed != NULL) {
        Py_DECREF(this->m_pPythonOnMidiEventProcessed);
        this->m_pPythonOnMidiEventProcessed = NULL;
    }
}

bool PyVoxelHorizon::InitializePython(const WCHAR* wchPyVoxelHorizonPath) {
    if (this->m_IsPythonInitialized) {
        return false;
    }

    Py_Initialize();

    PyObject* pPythonSysModule = PyImport_ImportModule("sys");

    if (pPythonSysModule == NULL)
    {
        if (!this->CrashIfPythonThrowException()) {
            this->CrashWithMessage(L"Failed to `PyImport_ImportModule(\"sys\") == NULL`.");
        }

        return false;
    }

    PyObject* pPythonSysPath = PyObject_GetAttrString(pPythonSysModule, "path");

    if (pPythonSysPath == NULL)
    {
        if (!this->CrashIfPythonThrowException()) {
            this->CrashWithMessage(L"Failed to `PyObject_GetAttrString(pPythonSysModule, \"path\") == NULL`.");
        }

        return false;
    }

    PyObject* pPythonScriptFileDirectoryPath = PyUnicode_FromWideChar(wchPyVoxelHorizonPath, wcsnlen_s(wchPyVoxelHorizonPath, MAX_PATH));

    if (pPythonScriptFileDirectoryPath == NULL)
    {
        if (!this->CrashIfPythonThrowException()) {
            this->CrashWithMessage(L"Failed to `PyUnicode_FromWideChar(wchPyVoxelHorizonPath, wcsnlen_s(wchPyVoxelHorizonPath, MAX_PATH)) == NULL`.");
        }

        return false;
    }

    PyList_Append(pPythonSysPath, pPythonScriptFileDirectoryPath);

    PyObject* pPythonVoxelHorizonModule = PyImport_ImportModule("entrypoint");

    if (pPythonVoxelHorizonModule == NULL)
    {
        if (!this->CrashIfPythonThrowException()) {
            this->CrashWithMessage(L"Failed to `PyImport_ImportModule(\"entrypoint\") == NULL`.");
        }

        return false;
    }

    PyObject* pPythonCreateGameHook = PyObject_GetAttrString(pPythonVoxelHorizonModule, "create_game_hook");

    if (pPythonCreateGameHook == NULL)
    {
        if (!this->CrashIfPythonThrowException()) {
            this->CrashWithMessage(L"Failed to `PyObject_GetAttrString(pPythonVoxelHorizonModule, \"GameHook\") == NULL`.");
        }

        return false;
    }

    PyObject* pPythonGameHookAddress = PyLong_FromUnsignedLongLong((PyAddress)this);

    if (pPythonGameHookAddress == NULL)
    {
        if (!this->CrashIfPythonThrowException()) {
            this->CrashWithMessage(L"Failed to `PyLong_FromUnsignedLongLong((PyAddress)this) == NULL`.");
        }

        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(1, pPythonGameHookAddress);

    if (pPythonArgument == NULL)
    {
        if (!this->CrashIfPythonThrowException()) {
            this->CrashWithMessage(L"Failed to `PyTuple_Pack(1, pPythonScriptFileDirectoryPath) == NULL`.");
        }

        return false;
    }

    this->m_pPythonGameHook = PyObject_Call(pPythonCreateGameHook, pPythonArgument, NULL);

    if (this->m_pPythonGameHook == NULL)
    {
        if (!this->CrashIfPythonThrowException()) {
            this->CrashWithMessage(L"Failed to `PyTuple_Pack(1, pPythonScriptFileDirectoryPath) == NULL`.");
        }

        return false;
    }

    this->m_pPythonOnStartScene = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_start_scene");
    this->m_pPythonOnRun = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_run");
    this->m_pPythonOnDestroyScene = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_destroy_scene");

    this->m_pPythonOnMouseLButtonDown = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_mouse_left_button_down");
    this->m_pPythonOnMouseLButtonUp = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_mouse_left_button_up");
    this->m_pPythonOnMouseRButtonDown = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_mouse_right_button_down");
    this->m_pPythonOnMouseRButtonUp = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_mouse_right_button_up");
    this->m_pPythonOnMouseMove = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_mouse_move");
    this->m_pPythonOnMouseMoveHV = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_mouse_move_hv");
    this->m_pPythonOnMouseWheel = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_mouse_wheel");

    this->m_pPythonOnKeyDown = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_key_down");
    this->m_pPythonOnKeyUp = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_key_up");
    this->m_pPythonOnCharUnicode = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_character_unicode");

    this->m_pPythonOnDPadLB = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_left_bumper_press");
    this->m_pPythonOffDPadLB = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_left_bumper_release");
    this->m_pPythonOnDPadRB = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_right_bumper_press");
    this->m_pPythonOffDPadRB = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_right_bumper_release");

    this->m_pPythonOnDPadUp = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_up_press");
    this->m_pPythonOnDPadDown = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_down_press");
    this->m_pPythonOnDPadLeft = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_left_press");
    this->m_pPythonOnDPadRight = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_right_press");
    this->m_pPythonOffDPadUp = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_up_release");
    this->m_pPythonOffDPadDown = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_down_release");
    this->m_pPythonOffDPadLeft = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_left_release");
    this->m_pPythonOffDPadRight = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_right_release");

    this->m_pPythonOnPadPressedA = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_a_press");
    this->m_pPythonOnPadPressedB = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_b_press");
    this->m_pPythonOnPadPressedX = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_x_press");
    this->m_pPythonOnPadPressedY = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_y_press");
    this->m_pPythonOffPadPressedA = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_a_release");
    this->m_pPythonOffPadPressedB = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_b_release");
    this->m_pPythonOffPadPressedX = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_x_release");
    this->m_pPythonOffPadPressedY = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_pad_y_release");

    this->m_pPythonOnKeyDownFunc = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_key_down_func");
    this->m_pPythonOnKeyDownCtrlFunc = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_key_down_control_func");

    this->m_pPythonOnPreConsoleCommand = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_console_command");

    this->m_pPythonOnMidiInput = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_midi_input");
    this->m_pPythonOnMidiEventProcessed = PyObject_GetAttrStringIfExists(this->m_pPythonGameHook, "on_midi_event_processed");

    this->m_IsPythonInitialized = true;

    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonCreateGameHook);
    Py_DECREF(pPythonVoxelHorizonModule);
    Py_DECREF(pPythonScriptFileDirectoryPath);
    Py_DECREF(pPythonSysPath);
    Py_DECREF(pPythonSysModule);

    return true;
}


void PyVoxelHorizon::ShowMessageBox(const WCHAR* wchTitle, const WCHAR* wchMessage, ...)
{
    va_list pArgument;
    va_start(pArgument, wchMessage);

    size_t length = _vscwprintf(wchMessage, pArgument);
    wchar_t* pBuffer = new wchar_t[length + 1];

    vswprintf_s(pBuffer, length + 1, wchMessage, pArgument);

    va_end(pArgument);

    MessageBoxW(NULL, pBuffer, wchTitle, MB_OK);

    delete[] pBuffer;
}

bool PyVoxelHorizon::ShowPythonException()
{
    if (!PyErr_Occurred())
    {
        return false;
    }

    PyObject* pPythonType;
    PyObject* pPythonValue;
    PyObject* pPythonTraceback;

    PyErr_Fetch(&pPythonType, &pPythonValue, &pPythonTraceback);

    if (pPythonType == NULL)
    {
        return false;
    }

    if (pPythonTraceback == NULL) {
        pPythonTraceback = Py_None;
    }

    PyErr_NormalizeException(&pPythonType, &pPythonValue, &pPythonTraceback);

    if (pPythonTraceback == NULL)
    {
        this->CrashWithMessage(L"Failed to `pPythonTraceback == NULL`.");
        return false;
    }

    PyException_SetTraceback(pPythonValue, pPythonTraceback);

    PyObject* pPythonTracebackModule = PyImport_ImportModule("traceback");

    if (pPythonTracebackModule == NULL)
    {
        this->CrashWithMessage(L"Failed to `PyImport_ImportModule(\"traceback\") == NULL`.");
        return false;
    }

    PyObject* pPythonFormatException = PyObject_GetAttrString(pPythonTracebackModule, "format_exception");

    if (pPythonFormatException == NULL)
    {
        this->CrashWithMessage(L"Failed to `PyObject_GetAttrString(pPythonTracebackModule, \"format_exception\") == NULL`.");
        return false;
    }

    PyObject* pPythonFormatResult = PyObject_CallObject(pPythonFormatException, PyTuple_Pack(3, pPythonType, pPythonValue, pPythonTraceback));

    if (pPythonFormatResult == NULL)
    {
        this->CrashWithMessage(L"Failed to `PyObject_CallObject(pPythonFormatException, PyTuple_Pack(3, pPythonType, pPythonValue, pPythonTraceback)) == NULL`.");
        return false;
    }

    PyObject* pPythonJoinResult = PyUnicode_Join(PyUnicode_FromString("\n"), pPythonFormatResult);

    if (pPythonJoinResult == NULL)
    {
        this->CrashWithMessage(L"Failed to `PyUnicode_Join(PyUnicode_FromString(\"\\n\"), pPythonFormatResult)`.");
        return false;
    }

    const char* message = PyUnicode_AsUTF8(pPythonJoinResult);

    this->ShowMessageBox(L"Python Exception", L"Exception in Python\r\n%S", message);

    return true;
}


void PyVoxelHorizon::CrashWithMessage(const WCHAR* wchMessage, ...)
{
    va_list pArgument;
    va_start(pArgument, wchMessage);

    this->ShowMessageBox(L"PyVoxelHorizon Crash", wchMessage, pArgument);

    va_end(pArgument);

    // delete this;
}

bool PyVoxelHorizon::CrashIfPythonThrowException()
{
    if (!this->ShowPythonException()) {
        return false;
    }

    // delete this;

    return true;
}


STDMETHODIMP PyVoxelHorizon::QueryInterface(REFIID refiid, void** ppv)
{
    *ppv = nullptr;

    return E_NOINTERFACE;
}

STDMETHODIMP_(ULONG) PyVoxelHorizon::AddRef()
{
    m_dwRefCount++;

    return m_dwRefCount;
}

STDMETHODIMP_(ULONG) PyVoxelHorizon::Release()
{
    DWORD ref_count = --m_dwRefCount;

    if (!m_dwRefCount) {
        delete this;
    }

    return ref_count;
}


void __stdcall PyVoxelHorizon::OnStartScene(IVHController* pVHController, IVHNetworkLayer* pNetworkLayer, const WCHAR* wchPluginPath)
{
    if (!this->m_IsPythonInitialized) {
        WCHAR wchPyVoxelHorizonPath[MAX_PATH];

        if (PathCombineW(wchPyVoxelHorizonPath, wchPluginPath, L"PyVoxelHorizon") == NULL) {
            this->CrashWithMessage(L"Failed to `PathCombineW(wchPyVoxelHorizonPath, wchPluginPath, L\"PyVoxelHorizon\")`.");
            return;
        }

        this->InitializePython(wchPyVoxelHorizonPath);
    }

    if (!this->m_IsPythonInitialized || this->m_pPythonOnStartScene == NULL) {
        return;
    }

    PyObject* pPythonVHControllerAddress = PyLong_FromUnsignedLongLong((PyAddress)pVHController);
    PyObject* pPythonNetworkLayerAddress = PyLong_FromUnsignedLongLong((PyAddress)pNetworkLayer);
    PyObject* pPythonPluginPath = PyUnicode_FromWideChar(wchPluginPath, wcsnlen_s(wchPluginPath, MAX_PATH));
    PyObject* pPythonArgument = PyTuple_Pack(3, pPythonVHControllerAddress, pPythonNetworkLayerAddress, pPythonPluginPath);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnStartScene, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return;
    }

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonPluginPath);
    Py_DECREF(pPythonNetworkLayerAddress);
    Py_DECREF(pPythonVHControllerAddress);
}

void __stdcall PyVoxelHorizon::OnRun()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnRun == NULL) {
        return;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnRun, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return;
    }

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
}

void __stdcall PyVoxelHorizon::OnDestroyScene()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnDestroyScene == NULL) {
        return;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnDestroyScene, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return;
    }

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
}


BOOL __stdcall PyVoxelHorizon::OnMouseLButtonDown(int x, int y, UINT nFlags)
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnMouseLButtonDown == NULL) {
        return false;
    }

    PyObject* pPythonX = PyLong_FromLong(x);
    PyObject* pPythonY = PyLong_FromLong(y);
    PyObject* pPythonNFlags = PyLong_FromUnsignedLong(nFlags);
    PyObject* pPythonArgument = PyTuple_Pack(3, pPythonX, pPythonY, pPythonNFlags);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnMouseLButtonDown, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonNFlags);
    Py_DECREF(pPythonY);
    Py_DECREF(pPythonX);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnMouseLButtonUp(int x, int y, UINT nFlags)
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnMouseLButtonUp == NULL) {
        return false;
    }

    PyObject* pPythonX = PyLong_FromLong(x);
    PyObject* pPythonY = PyLong_FromLong(y);
    PyObject* pPythonNFlags = PyLong_FromUnsignedLong(nFlags);
    PyObject* pPythonArgument = PyTuple_Pack(3, pPythonX, pPythonY, pPythonNFlags);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnMouseLButtonUp, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonNFlags);
    Py_DECREF(pPythonY);
    Py_DECREF(pPythonX);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnMouseRButtonDown(int x, int y, UINT nFlags)
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnMouseRButtonDown == NULL) {
        return false;
    }

    PyObject* pPythonX = PyLong_FromLong(x);
    PyObject* pPythonY = PyLong_FromLong(y);
    PyObject* pPythonNFlags = PyLong_FromUnsignedLong(nFlags);
    PyObject* pPythonArgument = PyTuple_Pack(3, pPythonX, pPythonY, pPythonNFlags);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnMouseRButtonDown, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonNFlags);
    Py_DECREF(pPythonY);
    Py_DECREF(pPythonX);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnMouseRButtonUp(int x, int y, UINT nFlags)
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnMouseRButtonUp == NULL) {
        return false;
    }

    PyObject* pPythonX = PyLong_FromLong(x);
    PyObject* pPythonY = PyLong_FromLong(y);
    PyObject* pPythonNFlags = PyLong_FromUnsignedLong(nFlags);
    PyObject* pPythonArgument = PyTuple_Pack(3, pPythonX, pPythonY, pPythonNFlags);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnMouseRButtonUp, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonNFlags);
    Py_DECREF(pPythonY);
    Py_DECREF(pPythonX);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnMouseMove(int x, int y, UINT nFlags)
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnMouseMove == NULL) {
        return false;
    }

    PyObject* pPythonX = PyLong_FromLong(x);
    PyObject* pPythonY = PyLong_FromLong(y);
    PyObject* pPythonNFlags = PyLong_FromUnsignedLong(nFlags);
    PyObject* pPythonArgument = PyTuple_Pack(3, pPythonX, pPythonY, pPythonNFlags);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnMouseMove, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonNFlags);
    Py_DECREF(pPythonY);
    Py_DECREF(pPythonX);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnMouseMoveHV(int iMoveX, int iMoveY, BOOL bLButtonPressed, BOOL bRButtonPressed, BOOL bMButtonPressed)
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnMouseMoveHV == NULL) {
        return false;
    }

    PyObject* pPythonMoveX = PyLong_FromLong(iMoveX);
    PyObject* pPythonMoveY = PyLong_FromLong(iMoveY);
    PyObject* pPythonLButtonPressed = PyBool_FromLong(bLButtonPressed);
    PyObject* pPythonRButtonPressed = PyBool_FromLong(bRButtonPressed);
    PyObject* pPythonMButtonPressed = PyBool_FromLong(bMButtonPressed);
    PyObject* pPythonArgument = PyTuple_Pack(5, pPythonMoveX, pPythonMoveY, pPythonLButtonPressed, pPythonRButtonPressed, pPythonMButtonPressed);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnMouseMoveHV, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonMButtonPressed);
    Py_DECREF(pPythonRButtonPressed);
    Py_DECREF(pPythonLButtonPressed);
    Py_DECREF(pPythonMoveY);
    Py_DECREF(pPythonMoveX);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnMouseWheel(int x, int y, int iWheel)
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnMouseWheel == NULL) {
        return false;
    }

    PyObject* pPythonX = PyLong_FromLong(x);
    PyObject* pPythonY = PyLong_FromLong(y);
    PyObject* pPythonWheel = PyLong_FromLong(iWheel);
    PyObject* pPythonArgument = PyTuple_Pack(3, pPythonX, pPythonY, pPythonWheel);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnMouseWheel, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonWheel);
    Py_DECREF(pPythonY);
    Py_DECREF(pPythonX);

    return returnValue;
}


BOOL __stdcall PyVoxelHorizon::OnKeyDown(UINT nChar)
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnKeyDown == NULL) {
        return false;
    }

    PyObject* pPythonChar = PyLong_FromUnsignedLong(nChar);
    PyObject* pPythonArgument = PyTuple_Pack(1, pPythonChar);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnKeyDown, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonChar);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnKeyUp(UINT nChar)
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnKeyUp == NULL) {
        return false;
    }

    PyObject* pPythonChar = PyLong_FromUnsignedLong(nChar);
    PyObject* pPythonArgument = PyTuple_Pack(1, pPythonChar);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnKeyUp, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonChar);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnCharUnicode(UINT nChar)
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnCharUnicode == NULL) {
        return false;
    }

    PyObject* pPythonChar = PyLong_FromUnsignedLong(nChar);
    PyObject* pPythonArgument = PyTuple_Pack(1, pPythonChar);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnCharUnicode, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonChar);

    return returnValue;
}


BOOL __stdcall PyVoxelHorizon::OnDPadLB()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnDPadLB == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnDPadLB, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OffDPadLB()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOffDPadLB == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOffDPadLB, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnDPadRB()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnDPadRB == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnDPadRB, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OffDPadRB()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOffDPadRB == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOffDPadRB, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}


BOOL __stdcall PyVoxelHorizon::OnDPadUp()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnDPadUp == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnDPadUp, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnDPadDown()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnDPadDown == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnDPadDown, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnDPadLeft()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnDPadLeft == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnDPadLeft, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnDPadRight()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnDPadRight == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnDPadRight, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OffDPadUp()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOffDPadUp == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOffDPadUp, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OffDPadDown()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOffDPadDown == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOffDPadDown, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OffDPadLeft()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOffDPadLeft == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOffDPadLeft, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OffDPadRight()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOffDPadRight == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOffDPadRight, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}


BOOL __stdcall PyVoxelHorizon::OnPadPressedA()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnPadPressedA == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnPadPressedA, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnPadPressedB()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnPadPressedB == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnPadPressedB, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnPadPressedX()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnPadPressedX == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnPadPressedX, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnPadPressedY()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnPadPressedY == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnPadPressedY, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OffPadPressedA()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOffPadPressedA == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOffPadPressedA, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OffPadPressedB()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOffPadPressedB == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOffPadPressedB, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OffPadPressedX()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOffPadPressedX == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOffPadPressedX, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OffPadPressedY()
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOffPadPressedY == NULL) {
        return false;
    }

    PyObject* pPythonArgument = PyTuple_Pack(0);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOffPadPressedY, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);

    return returnValue;
}


BOOL __stdcall PyVoxelHorizon::OnKeyDownFunc(UINT nChar)
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnKeyDownFunc == NULL) {
        return false;
    }

    PyObject* pPythonChar = PyLong_FromUnsignedLong(nChar);
    PyObject* pPythonArgument = PyTuple_Pack(1, pPythonChar);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnKeyDownFunc, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonChar);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnKeyDownCtrlFunc(UINT nChar)
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnKeyDownCtrlFunc == NULL) {
        return false;
    }

    PyObject* pPythonChar = PyLong_FromUnsignedLong(nChar);
    PyObject* pPythonArgument = PyTuple_Pack(1, pPythonChar);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnKeyDownCtrlFunc, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonChar);

    return returnValue;
}


BOOL __stdcall PyVoxelHorizon::OnPreConsoleCommand(const WCHAR* wchCmd, DWORD dwCmdLen)
{
    if (!this->m_IsPythonInitialized || this->m_pPythonOnPreConsoleCommand == NULL) {
        return false;
    }

    PyObject* pPythonCmd = PyUnicode_FromWideChar(wchCmd, dwCmdLen);
    PyObject* pPythonArgument = PyTuple_Pack(1, pPythonCmd);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnPreConsoleCommand, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonCmd);

    return returnValue;
}


BOOL __stdcall PyVoxelHorizon::OnMidiInput(const MIDI_MESSAGE_L* pMessage, BOOL bBroadcastMode, LARGE_INTEGER BeginCounter) {
    if (!this->m_IsPythonInitialized || this->m_pPythonOnMidiInput == NULL) {
        return false;
    }

    PyObject* pPythonMidiMessageAddress = PyLong_FromUnsignedLongLong((PyAddress)pMessage);
    PyObject* pPythonBroadcastMode = PyBool_FromLong(bBroadcastMode);
    PyObject* pPythonBeginCounter = PyLong_FromLongLong(BeginCounter.QuadPart);
    PyObject* pPythonArgument = PyTuple_Pack(3, pPythonMidiMessageAddress, pPythonBroadcastMode, pPythonBeginCounter);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnMidiInput, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonBeginCounter);
    Py_DECREF(pPythonBroadcastMode);
    Py_DECREF(pPythonMidiMessageAddress);

    return returnValue;
}

BOOL __stdcall PyVoxelHorizon::OnMidiEventProcessed(const MIDI_MESSAGE_L* pMessage, MIDI_EVENT_FROM_TYPE FromType) {
    if (!this->m_IsPythonInitialized || this->m_pPythonOnMidiEventProcessed == NULL) {
        return false;
    }

    PyObject* pPythonMidiMessageAddress = PyLong_FromUnsignedLongLong((PyAddress)pMessage);
    PyObject* pPythonMidiEventFromType = PyLong_FromLong((long)FromType);
    PyObject* pPythonArgument = PyTuple_Pack(2, pPythonMidiMessageAddress, pPythonMidiEventFromType);
    PyObject* pPythonReturnValue = PyObject_CallObject(this->m_pPythonOnMidiEventProcessed, pPythonArgument);

    if (pPythonReturnValue == NULL)
    {
        this->ShowPythonException();
        return false;
    }

    bool returnValue = PyObject_IsTrue(pPythonReturnValue);

    Py_DECREF(pPythonReturnValue);
    Py_DECREF(pPythonArgument);
    Py_DECREF(pPythonMidiEventFromType);
    Py_DECREF(pPythonMidiMessageAddress);

    return returnValue;
}