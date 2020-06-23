package crc64090cf482a1d08823;


public class CameraCaptureStillPictureSessionCallback
	extends android.hardware.camera2.CameraCaptureSession.CaptureCallback
	implements
		mono.android.IGCUserPeer
{
/** @hide */
	public static final String __md_methods;
	static {
		__md_methods = 
			"n_onCaptureCompleted:(Landroid/hardware/camera2/CameraCaptureSession;Landroid/hardware/camera2/CaptureRequest;Landroid/hardware/camera2/TotalCaptureResult;)V:GetOnCaptureCompleted_Landroid_hardware_camera2_CameraCaptureSession_Landroid_hardware_camera2_CaptureRequest_Landroid_hardware_camera2_TotalCaptureResult_Handler\n" +
			"";
		mono.android.Runtime.register ("Camera2Basic.Listeners.CameraCaptureStillPictureSessionCallback, Camera2Basic", CameraCaptureStillPictureSessionCallback.class, __md_methods);
	}


	public CameraCaptureStillPictureSessionCallback ()
	{
		super ();
		if (getClass () == CameraCaptureStillPictureSessionCallback.class)
			mono.android.TypeManager.Activate ("Camera2Basic.Listeners.CameraCaptureStillPictureSessionCallback, Camera2Basic", "", this, new java.lang.Object[] {  });
	}

	public CameraCaptureStillPictureSessionCallback (crc64b678081366886b9e.Camera2BasicFragment p0)
	{
		super ();
		if (getClass () == CameraCaptureStillPictureSessionCallback.class)
			mono.android.TypeManager.Activate ("Camera2Basic.Listeners.CameraCaptureStillPictureSessionCallback, Camera2Basic", "Camera2Basic.Camera2BasicFragment, Camera2Basic", this, new java.lang.Object[] { p0 });
	}


	public void onCaptureCompleted (android.hardware.camera2.CameraCaptureSession p0, android.hardware.camera2.CaptureRequest p1, android.hardware.camera2.TotalCaptureResult p2)
	{
		n_onCaptureCompleted (p0, p1, p2);
	}

	private native void n_onCaptureCompleted (android.hardware.camera2.CameraCaptureSession p0, android.hardware.camera2.CaptureRequest p1, android.hardware.camera2.TotalCaptureResult p2);

	private java.util.ArrayList refList;
	public void monodroidAddReference (java.lang.Object obj)
	{
		if (refList == null)
			refList = new java.util.ArrayList ();
		refList.add (obj);
	}

	public void monodroidClearReferences ()
	{
		if (refList != null)
			refList.clear ();
	}
}
