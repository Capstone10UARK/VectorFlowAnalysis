import java.util.*;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.awt.Color;
import java.text.DecimalFormat;
import java.io.IOException;
import java.io.File;
import java.lang.*;

class ImageProcessor extends Thread {
    //when executing on linux this path must use / instead of \ otherwise this causes a NullPointerException
    public ProgressWrapper progress;
    
    private static final String IMAGE_DIRECTORY_PATH = "/images/testerImages";
    private String outputPath;

    public ImageProcessor(String outputPathPassed, ProgressWrapper progressPassed) throws IOException {
        VFI_Map.Init();
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
		long startTime = System.currentTimeMillis();

		File[] listOfImages = getListOfImages();

		for (int frameIndex = 0; frameIndex < listOfImages.length; frameIndex++) {
			File imageFile = listOfImages[frameIndex];
			BufferedImage loadedImage = null;

			try {
				loadedImage = ImageIO.read(imageFile);
				writer.writeOneFile(processSingleImage(loadedImage), frameIndex);
			} catch (IOException e) {
			    System.out.println("Failed to load file index " + Integer.toString(frameIndex));
			}
			progress.setProgress((float)(frameIndex+1) / listOfImages.length);
		}

		printProcessingTime(startTime);
	}

	private File[] getListOfImages() {
		String directory = System.getProperty("user.dir");
		File parentDirectory = new File(directory).getParentFile();
		
		File directoryOfImages = new File(parentDirectory.getAbsolutePath() + IMAGE_DIRECTORY_PATH);
		File[] listOfImages = directoryOfImages.listFiles();
		return listOfImages;
	}

	private void printProcessingTime(long startTime) {
		long processingTimeMs = System.currentTimeMillis() - startTime;
		long processingTimeS = processingTimeMs / 1000;
		long processingTimeMin = processingTimeS / 60;
		processingTimeS = processingTimeS % 60;
		System.out.println("Processing took " + processingTimeMin + " minutes and " + processingTimeS + " seconds.");
	}
	
	private ArrayList<Map> processSingleImage(BufferedImage imageToProcess) {
        
		ArrayList<Map> listOfVectors = new ArrayList<Map>();

		for(int y = 0; y < imageToProcess.getHeight(); y++)
		{
			for(int x = 0; x < imageToProcess.getWidth(); x++)
			{
				Color c = new Color(imageToProcess.getRGB(x, y));
				int color = imageToProcess.getRGB(x, y);
				float[] hsv = new float[3];

				Color.RGBtoHSB(c.getRed(), c.getGreen(), c.getBlue(), hsv);
				//If the color is not gray scale (aka "is color")
				if((hsv[1] > 0.2)&&(hsv[2] > 0.2))
				{
					HashMap vector = new HashMap();
					vector.put("x", x);
					vector.put("y", y);
					vector.put("Vx", truncate(VFI_Map.getVx(color)));
					vector.put("Vy", truncate(VFI_Map.getVy(color)));
					vector.put("speed", truncate(VFI_Map.getVelocity(color)));
					listOfVectors.add(vector);
				}
			}
		}
		System.out.println("Finished processing single image");
		
		return listOfVectors;
	}
   
    private double truncate(double value) {
		DecimalFormat df = new DecimalFormat("#.##");
		String trunc = df.format(value);

		return Double.parseDouble(trunc);
    }   
}
