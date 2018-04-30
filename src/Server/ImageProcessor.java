import java.util.*;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.awt.Color;
import java.text.DecimalFormat;
import java.io.IOException;
import java.io.File;
import java.lang.*;

class ImageProcessor extends Thread implements ThreadCompleteListener{
    //when executing on linux this path must use / instead of \ otherwise this causes a NullPointerException
    
    private String outputPath;
    private String imageDirectoryPath;
    private ProgressWrapper progress;
    private VFI_Map vfi;
    private int numberOfImages;
    private int completedImages = 0;
    private long startTime;

    public ImageProcessor(String outputPathPassed, ProgressWrapper progressPassed) throws IOException {
        vfi = new VFI_Map();
        imageDirectoryPath = outputPathPassed + "/Frames";
        outputPath = outputPathPassed;
        progress = progressPassed;
    }

    public void run(){
        try {
        	CsvWriter writer = new CsvWriter(outputPath);
    	    processEntireSelection(writer);
        } catch (IOException e) {
            System.out.println("couldn't start processing");
        }
    }

	private void processEntireSelection(CsvWriter writer) throws IOException{
        startTime = System.currentTimeMillis();

        File[] listOfImages = getListOfImages();
        numberOfImages = listOfImages.length;

        for (int frameIndex = 0; frameIndex < numberOfImages; frameIndex++) {
            File imageFile = listOfImages[frameIndex];
            BufferedImage loadedImage = null;

            try {
                loadedImage = ImageIO.read(imageFile);
                NotifyingRunnable runner = new SingleImageRunnable(vfi, writer, frameIndex, loadedImage);
                runner.addListener(this);
                Thread thread = new Thread(runner);
                thread.start();

            } catch (IOException e) {
                System.out.println("Failed to load file index " + Integer.toString(frameIndex));
            }
            
        }
    }

	private File[] getListOfImages() {
		File directoryOfImages = new File(imageDirectoryPath);
		File[] listOfImages = directoryOfImages.listFiles();
		return listOfImages;
	}

	private void printProcessingTime() {
		long processingTimeMs = System.currentTimeMillis() - startTime;
		long processingTimeS = processingTimeMs / 1000;
		long processingTimeMin = processingTimeS / 60;
		processingTimeS = processingTimeS % 60;
		System.out.println("Processing took " + processingTimeMin + " minutes and " + processingTimeS + " seconds.");
  }
   
    public void threadComplete(Runnable runner) {
        completedImages = completedImages + 1;
        float newProgress = (float)completedImages / numberOfImages;
        progress.setProgress(newProgress);
        if(newProgress == 1)
            printProcessingTime();
    }
}
