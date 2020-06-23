package crc64b678081366886b9e;


public class ConfirmationDialog_PositiveListener
	extends java.lang.Object
	implements
		mono.android.IGCUserPeer,
		android.content.DialogInterface.OnClickListener
{
/** @hide */
	public static final String __md_methods;
	static {
		__md_methods = 
			"n_onClick:(Landroid/content/DialogInterface;I)V:GetOnClick_Landroid_content_DialogInterface_IHandler:Android.Content.IDialogInterfaceOnClickListenerInvoker, Mono.Android, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null\n" +
			"";
		mono.android.Runtime.register ("Camera2Basic.ConfirmationDialog+PositiveListener, Camera2Basic", ConfirmationDialog_PositiveListener.class, __md_methods);
	}


	public ConfirmationDialog_PositiveListener ()
	{
		super ();
		if (getClass () == ConfirmationDialog_PositiveListener.class)
			mono.android.TypeManager.Activate ("Camera2Basic.ConfirmationDialog+PositiveListener, Camera2Basic", "", this, new java.lang.Object[] {  });
	}


	public void onClick (android.content.DialogInterface p0, int p1)
	{
		n_onClick (p0, p1);
	}

	private native void n_onClick (android.content.DialogInterface p0, int p1);

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
