package com.personal_project.exam_management_system.config;

import org.hibernate.dialect.Dialect;
import org.hibernate.dialect.SQLServerDialect;

public class SQLiteDialect extends Dialect {
    public SQLiteDialect() {
        super();
        // Implement necessary dialect features for SQLite here
    }

//    @Override
    public boolean supportsIdentityColumns() {
        return true;
    }

//    @Override
    public boolean supportsInsertSelectIdentity() {
        return true;
    }

    // Implement other necessary methods
}
