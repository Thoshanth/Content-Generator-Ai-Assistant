package com.contentgen.config;

import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.JsonSerializer;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.databind.module.SimpleModule;
import com.google.cloud.Timestamp;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.converter.json.Jackson2ObjectMapperBuilder;

import java.io.IOException;
import java.time.Instant;

@Configuration
public class JacksonConfig {

    @Bean
    public Jackson2ObjectMapperBuilder jackson2ObjectMapperBuilder() {
        return new Jackson2ObjectMapperBuilder()
                .modules(firestoreTimestampModule());
    }

    @Bean
    public SimpleModule firestoreTimestampModule() {
        SimpleModule module = new SimpleModule();
        module.addSerializer(Timestamp.class, new TimestampSerializer());
        module.addDeserializer(Timestamp.class, new TimestampDeserializer());
        return module;
    }

    public static class TimestampSerializer extends JsonSerializer<Timestamp> {
        @Override
        public void serialize(Timestamp timestamp, JsonGenerator gen, SerializerProvider serializers) throws IOException {
            if (timestamp == null) {
                gen.writeNull();
            } else {
                // Convert to ISO 8601 string format for frontend compatibility
                Instant instant = Instant.ofEpochSecond(timestamp.getSeconds(), timestamp.getNanos());
                gen.writeString(instant.toString());
            }
        }
    }

    public static class TimestampDeserializer extends JsonDeserializer<Timestamp> {
        @Override
        public Timestamp deserialize(JsonParser p, DeserializationContext ctxt) throws IOException {
            String value = p.getValueAsString();
            if (value == null || value.isEmpty()) {
                return null;
            }
            try {
                Instant instant = Instant.parse(value);
                return Timestamp.ofTimeSecondsAndNanos(instant.getEpochSecond(), instant.getNano());
            } catch (Exception e) {
                // Fallback: try to parse as epoch seconds
                try {
                    long epochSeconds = Long.parseLong(value);
                    return Timestamp.ofTimeSecondsAndNanos(epochSeconds, 0);
                } catch (NumberFormatException nfe) {
                    throw new IOException("Unable to parse timestamp: " + value, e);
                }
            }
        }
    }
}