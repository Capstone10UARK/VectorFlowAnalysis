import java.io.File;
import java.util.*;
import java.io.PrintWriter;
import java.io.IOException;
import java.io.FileNotFoundException;

class CsvWriter {
    
	private String outString;

    public CsvWriter(String outputPath) {
    	outString = outputPath;
    	File outputBaseDirectory = createNewDirectoryIfNotExist(outString);
    }

	public void writeOneFile(ArrayList<Map> listOfVectors, int frameNumber) {
		// create new directory for each second in the video
		int secondIndex = frameNumber / 24;
		String secondsFileString = outString + Integer.toString(secondIndex) + "/";
		File secondsFileDirectory = createNewDirectoryIfNotExist(secondsFileString);

		// create a new csc file for each frame
		File outputFile = new File(secondsFileString + Integer.toString(frameNumber) + ".csv");

		try {
			PrintWriter printWriter = new PrintWriter(outputFile);
			
			String headers = makeHeaders();
			printWriter.println(headers);

			for (int vectorIndex = 0; vectorIndex < listOfVectors.size(); vectorIndex++) {
				Map<String, Double> vector = listOfVectors.get(vectorIndex);
				printWriter.println(frameNumber + "," + vectorIndex + "," + vector.get("x") + "," + 
					vector.get("y") + "," + vector.get("Vx") + "," + vector.get("Vy") + "," + vector.get("speed"));
			}

			printWriter.close();
		} catch (FileNotFoundException e) {
			System.out.println("Output CSV file not found.");
		}
	}

	private File createNewDirectoryIfNotExist(String directoryString) {
		File directoryFile = new File(directoryString);
		if (!directoryFile.exists()) {
			directoryFile.mkdir();
		}
		return directoryFile;
	}

	private String makeHeaders() {
		StringBuilder sb = new StringBuilder();
		sb.append("Frame Index");
		sb.append(',');
		sb.append("Vector Index");
		sb.append(',');
		sb.append("X");
		sb.append(",");
		sb.append("Y");
		sb.append(",");
		sb.append("Vx");
		sb.append(",");
		sb.append("Vy");
		sb.append(",");
		sb.append("Speed");
		sb.append('\n');
		return(sb.toString());
	}
}
