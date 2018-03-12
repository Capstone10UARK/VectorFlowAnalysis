import java.util.Comparator;
import java.awt.Color;

class RGBComparator implements Comparator<Color>{

	public RGBComparator(){}
	
	@Override
	public int compare(Color c1, Color c2){
		if(c1.getRed() < c2.getRed())
			return -1;
		else if(c1.getRed() > c2.getRed())
			return 1;
		else if(c1.getGreen() < c2.getGreen())
			return -1;
		else if(c1.getGreen() > c2.getGreen())
			return 1;
		else if(c1.getBlue() < c2.getBlue())
			return -1;
		else if(c1.getBlue() > c2.getBlue())
			return 1;
		else
			return 0;
	}

	// public boolean equals(Object obj){
	// 	return false;
	// }
}