import java.util.*;
import java.awt.image.BufferedImage;
import java.awt.Color;
import java.text.DecimalFormat;

class SingleImageRunnable extends NotifyingRunnable {

    private static VFI_Map vfi;
    private CsvWriter writer;
    public int frameIndex;
    private BufferedImage loadedImage;

    public SingleImageRunnable(VFI_Map vfiPassed, CsvWriter writerPassed, int frameIndexPassed, BufferedImage loadedImagePassed) {
        vfi = vfiPassed;
        writer = writerPassed;
        frameIndex = frameIndexPassed;
        loadedImage = loadedImagePassed; 
    }

    public void doWork() {
        writer.writeOneFile(processSingleImage(loadedImage), frameIndex);
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
                    // get the rgb value closes to one represented in the RGB to vector data maps
                    int closestColor = vfi.searchMap(color);
                    HashMap vector = new HashMap();
                    vector.put("x", x);
                    vector.put("y", y);
                    vector.put("Vx", truncate(vfi.getVx(closestColor)));
                    vector.put("Vy", truncate(vfi.getVy(closestColor)));
                    vector.put("speed", truncate(vfi.getVelocity(closestColor)));
                    listOfVectors.add(vector);
                }
            }
        }
        
        return listOfVectors;
    }
   
    private double truncate(double value) {
        DecimalFormat df = new DecimalFormat("#.##");
        String trunc = df.format(value);

        return Double.parseDouble(trunc);
    }   
}