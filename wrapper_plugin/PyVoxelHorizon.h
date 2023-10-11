#ifndef PY_VOXEL_HORIZON_H
#define PY_VOXEL_HORIZON_H

#include "pch.h"

class PyVoxelHorizon : public IGameHook {
private:
	DWORD	m_dwRefCount = 1;

public:
	PyVoxelHorizon();
	~PyVoxelHorizon();

	STDMETHODIMP				QueryInterface(REFIID, void** ppv);
	STDMETHODIMP_(ULONG)		AddRef();
	STDMETHODIMP_(ULONG)		Release();

	void __stdcall	OnStartScene(IVHController* pVHController, IVHNetworkLayer* pNetworkLayer, const WCHAR* wchPluginPath);
	void __stdcall	OnRun();
	void __stdcall	OnDestroyScene();

	BOOL __stdcall	OnMouseLButtonDown(int x, int y, UINT nFlags);
	BOOL __stdcall	OnMouseLButtonUp(int x, int y, UINT nFlags);
	BOOL __stdcall	OnMouseRButtonDown(int x, int y, UINT nFlags);
	BOOL __stdcall	OnMouseRButtonUp(int x, int y, UINT nFlags);
	BOOL __stdcall	OnMouseMove(int x, int y, UINT nFlags);
	BOOL __stdcall	OnMouseMoveHV(int iMoveX, int iMoveY, BOOL bLButtonPressed, BOOL bRButtonPressed, BOOL bMButtonPressed);
	BOOL __stdcall	OnMouseWheel(int iWheel);

	BOOL __stdcall	OnKeyDown(UINT nChar);
	BOOL __stdcall	OnKeyUp(UINT nChar);
	BOOL __stdcall	OnCharUnicode(UINT nChar);

	BOOL __stdcall	OnDPadLB();
	BOOL __stdcall	OffDPadLB();
	BOOL __stdcall	OnDPadRB();
	BOOL __stdcall	OffDPadRB();

	BOOL __stdcall	OnDPadUp();
	BOOL __stdcall	OnDPadDown();
	BOOL __stdcall	OnDPadLeft();
	BOOL __stdcall	OnDPadRight();
	BOOL __stdcall	OffDPadUp();
	BOOL __stdcall	OffDPadDown();
	BOOL __stdcall	OffDPadLeft();
	BOOL __stdcall	OffDPadRight();

	BOOL __stdcall	OnPadPressedA();
	BOOL __stdcall	OnPadPressedB();
	BOOL __stdcall	OnPadPressedX();
	BOOL __stdcall	OnPadPressedY();
	BOOL __stdcall	OffPadPressedA();
	BOOL __stdcall	OffPadPressedB();
	BOOL __stdcall	OffPadPressedX();
	BOOL __stdcall	OffPadPressedY();

	BOOL __stdcall	OnKeyDownFunc(UINT nChar);
	BOOL __stdcall	OnKeyDownCtrlFunc(UINT nChar);
	BOOL __stdcall	OnPreConsoleCommand(const WCHAR* wchCmd, DWORD dwCmdLen);
};

#endif