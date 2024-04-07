DECLARE @DatabaseName nvarchar(50)
SET @DatabaseName = N'TeamReporting'  -- replace with your database name

DECLARE @SQL varchar(max)

SELECT @SQL = COALESCE(@SQL,'') + 'KILL ' + CONVERT(varchar(10), spid) + '; '
FROM master..sysprocesses 
WHERE dbid = DB_ID(@DatabaseName) AND spid <> @@SPID

EXEC(@SQL)