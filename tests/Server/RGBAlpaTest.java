import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import java.io.IOException;

class RGBAlpaTest{
	public static void main(String[] args){
		File file = new File("../images/colorKey.png");
		BufferedImage image;
		try{
			image = ImageIO.read(file);
		}
		catch(IOException e){
			System.out.println("Couldn't read Image");
			return;
		}

		for(int i = 0; i < image.getHeight(); i++){
			for(int j = 0; j < image.getWidth(); j++){
				int argb = image.getRGB(i,j);
				Color color = new Color(argb, true);
				if(color.getAlpha() != 255)
					System.out.println(color.getAlpha());
			}
		}
	}
}