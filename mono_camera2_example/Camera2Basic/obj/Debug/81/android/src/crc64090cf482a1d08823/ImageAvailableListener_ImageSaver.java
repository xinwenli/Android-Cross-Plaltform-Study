package crc64090cf482a1d08823;


public class ImageAvailableListener_ImageSaver
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
		mono.android.Runtime.register ("Camera2Basic.Listeners.ImageAvailableListener+ImageSaver, Camera2Basic", ImageAvailableListener_ImageSaver.class, __md_methods);
	}


	public ImageAvailableListener_ImageSaver ()
	{
		super ();
		if (getClass () == ImageAvailableListener_ImageSaver.class)
			mono.android.TypeManager.Activate ("Camera2Basic.Listeners.ImageAvailableListener+ImageSaver, Camera2Basic", "", this, new java.lang.Object[] {  });
	}

	public ImageAvailableListener_ImageSaver (android.media.Image p0, java.io.File p1)
	{
		super ();
		if (getClass () == ImageAvailableListener_ImageSaver.class)
			mono.android.TypeManager.Activate ("Camera2Basic.Listeners.ImageAvailableListener+ImageSaver, Camera2Basic", "Android.Media.Image, Mono.Android:Java.IO.File, Mono.Android", this, new java.lang.Object[] { p0, p1 });
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
