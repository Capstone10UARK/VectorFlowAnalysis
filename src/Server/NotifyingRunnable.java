import java.util.*;

public abstract class NotifyingRunnable implements Runnable {
    
    public abstract void doWork();

    
    private java.util.List<ThreadCompleteListener> listeners = Collections.synchronizedList( new ArrayList<ThreadCompleteListener>() );

    public final void addListener(final ThreadCompleteListener listener) {
        listeners.add(listener);
    }

    public void removeListener(ThreadCompleteListener listener) {
        listeners.remove(listener);
    }

    private final void notifyListeners() {
        synchronized (listeners) {
            for (ThreadCompleteListener listener : listeners) {
                listener.threadComplete(this);
            }
        }
    }

    public void run() {
        doWork();
        notifyListeners();
    }
}
