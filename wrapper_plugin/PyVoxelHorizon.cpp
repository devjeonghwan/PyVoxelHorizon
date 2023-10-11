#include "pch.h"
#include "PyVoxelHorizon.h"

PyVoxelHorizon::PyVoxelHorizon()
{
	#ifdef _DEBUG
		_CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
	#endif

    return;
}

PyVoxelHorizon::~PyVoxelHorizon()
{
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
	pVHController->WriteTextToSystemDlgW(0xFFFF00FF, L"This is PyVoxelHorizon!");
}

void __stdcall PyVoxelHorizon::OnRun()
{
}

void __stdcall PyVoxelHorizon::OnDestroyScene()
{
}


BOOL __stdcall PyVoxelHorizon::OnMouseLButtonDown(int x, int y, UINT nFlags)
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnMouseLButtonUp(int x, int y, UINT nFlags)
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnMouseRButtonDown(int x, int y, UINT nFlags)
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnMouseRButtonUp(int x, int y, UINT nFlags)
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnMouseMove(int x, int y, UINT nFlags)
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnMouseMoveHV(int iMoveX, int iMoveY, BOOL bLButtonPressed, BOOL bRButtonPressed, BOOL bMButtonPressed)
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnMouseWheel(int iWheel)
{
	return 0;
}


BOOL __stdcall PyVoxelHorizon::OnKeyDown(UINT nChar)
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnKeyUp(UINT nChar)
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnCharUnicode(UINT nChar)
{
	return 0;
}


BOOL __stdcall PyVoxelHorizon::OnDPadLB()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OffDPadLB()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnDPadRB()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OffDPadRB()
{
	return 0;
}


BOOL __stdcall PyVoxelHorizon::OnDPadUp()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnDPadDown()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnDPadLeft()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnDPadRight()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OffDPadUp()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OffDPadDown()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OffDPadLeft()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OffDPadRight()
{
	return 0;
}


BOOL __stdcall PyVoxelHorizon::OnPadPressedA()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnPadPressedB()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnPadPressedX()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnPadPressedY()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OffPadPressedA()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OffPadPressedB()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OffPadPressedX()
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OffPadPressedY()
{
	return 0;
}


BOOL __stdcall PyVoxelHorizon::OnKeyDownFunc(UINT nChar)
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnKeyDownCtrlFunc(UINT nChar)
{
	return 0;
}

BOOL __stdcall PyVoxelHorizon::OnPreConsoleCommand(const WCHAR* wchCmd, DWORD dwCmdLen)
{
	return 0;
}
