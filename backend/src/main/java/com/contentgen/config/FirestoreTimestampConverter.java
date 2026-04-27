package com.contentgen.config;

import com.google.cloud.Timestamp;
import com.google.cloud.firestore.annotation.PropertyName;

import java.util.Date;
import java.util.Map;

public class FirestoreTimestampConverter {
    
    /**
     * Convert Firestore timestamp (which can be a Map or Timestamp) to Timestamp
     */
    public static Timestamp convertToTimestamp(Object value) {
        if (value == null) {
            return null;
        }
        
        if (value instanceof Timestamp) {
            return (Timestamp) value;
        }
        
        if (value instanceof Map) {
            Map<String, Object> map = (Map<String, Object>) value;
            if (map.containsKey("_seconds")) {
                long seconds = ((Number) map.get("_seconds")).longValue();
                int nanos = map.containsKey("_nanoseconds") 
                    ? ((Number) map.get("_nanoseconds")).intValue() 
                    : 0;
                return Timestamp.ofTimeSecondsAndNanos(seconds, nanos);
            }
        }
        
        if (value instanceof Date) {
            Date date = (Date) value;
            return Timestamp.of(date);
        }
        
        if (value instanceof Long) {
            return Timestamp.ofTimeSecondsAndNanos((Long) value, 0);
        }
        
        return null;
    }
}
