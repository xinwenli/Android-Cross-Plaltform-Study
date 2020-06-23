package crc64b678081366886b9e;


public class Camera2BasicFragment_ShowToastRunnable
	extends java.lang.Object
	implements
		mono.android.IGCUserPeer,
		java.lang.Runnable
{
/** @hide */
	public static final String __md_methods;
	static {
		__md_methods = 
			"n_run:()V:GetRunHandler:Java.Lang.IRunnableInvoker, Mono.Android, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null\n" +
			"";
		mono.android.Runtime.register ("Camera2Basic.Camera2BasicFragment+ShowToastRunnable, Camera2Basic", Camera2BasicFragment_ShowToastRunnable.class, __md_methods);
	}


	public Camera2BasicFragment_ShowToastRunnable ()
	{
		super ();
		if (getClass () == Camera2BasicFragment_ShowToastRunnable.class)
			mono.android.TypeManager.Activate ("Camera2Basic.Camera2BasicFragment+ShowToastRunnable, Camera2Basic", "", this, new java.lang.Object[] {  });
	}

	public Camera2BasicFragment_ShowToastRunnable (android.content.Context p0, java.lang.String p1)
	{
		super ();
		if (getClass () == Camera2BasicFragment_ShowToastRunnable.class)
			mono.android.TypeManager.Activate ("Camera2Basic.Camera2BasicFragment+ShowToastRunnable, Camera2Basic", "Android.Content.Context, Mono.Android:System.String, mscorlib", this, new java.lang.Object[] { p0, p1 });
	}


	public void run ()
	{
		n_run ();
	}

	private native void n_run ();

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
