-- Active: 1712507441240@@127.0.0.1@1433
USE MASTER;
IF(EXISTS(SELECT * FROM sys.databases where name='TeamReporting'))
begin
    drop database TeamReporting
end

Create database TeamReporting

USE TeamReporting

CREATE TABLE Issue (
    [Key] nvarchar(10) not null primary KEY,
    [Summary] nvarchar(max) not null,
    [storyPoints] int null,
    [Status] nvarchar(50) not null,
    [Assignee] nvarchar(50) null,
    [Reporter] nvarchar(50) null,
    [Created] datetime null,
    [Updated] datetime null,
    [Resolved] datetime null
)
