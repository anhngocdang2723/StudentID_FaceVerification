package com.personal_project.exam_management_system.converter;

import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

@Converter(autoApply = true)
public class LocalDateConverter implements AttributeConverter<LocalDate, String> {

    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");

    @Override
    public String convertToDatabaseColumn(LocalDate date) {
        return (date == null ? null : date.format(formatter));
    }

    @Override
    public LocalDate convertToEntityAttribute(String date) {
        return (date == null ? null : LocalDate.parse(date, formatter));
    }
}
