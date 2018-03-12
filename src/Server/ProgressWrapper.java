class ProgressWrapper {
    float progress;

    public ProgressWrapper() {
        progress = 0;
    }

   	public void setProgress(float setTo) {
   		progress = setTo;
   		System.out.println("progress set to " + setTo);
   	}

   	public float getProgress() {
   		return progress;
   	}
}
