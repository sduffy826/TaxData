# Overview 
The code here was used to load the spreadsheets that I maintained for tax purposes into mysql tables.  Take a 
look at the sample spreadsheet.  You'll notice
- I summarize by category 
- You need to have values in at least one column in the spreadsheet otherwise pandas will ignore the column
- The column headers in the spreadsheet must match, I use that to pull values 

Once you have all the data loaded, and you created the tax_summary table you can get the data into a spreadsheet to view/analyze, or use data in mysql.

### There are different tables, here's a little on them (see ddic section for more)
- The tax_category table has the valid categories and flags to identiy what type of data it is.
- Over the years I used different categories in the spreadsheets, to get around that I have table tax_category_remap; when the spreadsheet is read it'll remap categories to the remapped name.  This saves you from having to re-edit each spreadsheet.
- The tax_detail table has the detail data from the spreadsheets.  
- The tax_summary table has the summarized data for each year we have.  If you want other years you need to make some trivial changes (see DDIC section for more and for more details on the tables).
- I added the tax_misc table, it has miscellaneous items.  Things like sep contribution, taxes bill for years (sometimes I prepaid taxes and wanted to know the bill amount), etc...

### DDIC
```
-- This table has all the valid categories (it'll have the remapped name if applicable (not val in spreadsheet))
drop table if exists `<dbname>`.`tax_category`;
create table `<dbname>`.`tax_category` (
  `id` integer not null auto_increment,
  `category` varchar(64) not null,
  `isExpense` char(1) not null,   -- Y-es (i.e. deposits are blank)
  `reportCode` char(1) not null,  -- A-Accountant etc...
  `livingExpense` char(1) not null, -- Y-es (meaning required annually)
  primary key (`id`)
)
ENGINE = InnoDB;

-- This table has the categories that need to be remppaed 
drop table if exists `<dbname>`.`tax_category_remap`;
create table `<dbname>`.`tax_category_remap` (
  `category` varchar(64) not null,
  `remappedCategory` varchar(64) not null,
  primary key (`category`)
)
ENGINE = InnoDB;

-- This table has the detail from the spreadsheet
drop table if exists `<dbname>`.`tax_detail`;
create table `<dbname>`.`tax_detail` (
  `id` integer not null auto_increment,
  `taxYear` smallint not null,
  `sheetName` varchar(32) not null,
  `itemDate` date not null,
  `description` varchar(128) not null,
  `amount` decimal(11,2) not null,
  `category` varchar(64) not null,
  `notesRef` varchar(128) not null,
  `notesRefSub` varchar(128) not null,
  `source` varchar(128) not null,
  `lineNumber` integer not null,
  `lineSubNumber` smallint,
  `runningTotal` decimal(11,2),
  `frequency` integer not null,
  `refOrCheckNum` varchar(64) not null,
  `memoOrIdentifier` varchar(64) not null,
  `iagCode` varchar(32) not null,
  `iagIdentifier` varchar(32) not null,
  `break` char(1) not null,tax_detail
  primary key (`id`)
)
ENGINE = InnoDB;

-- Has summarized data for category and each year of data.
-- If you want to have different years then you need to do two things:
--   alter this table and add/remove the year you want
--   change the mySqlSummaryTable.py and change the 'yearsOfData' list so that it has the years you want
--   
drop table if exists `<dbname>`.`tax_summary`;
create table `<dbname>`.`tax_summary` (
  `id` integer not null auto_increment,
  `category` varchar(64) not null,
  '2016' decimal(11,2) not null,
  '2017' decimal(11,2) not null,
  '2018' decimal(11,2) not null,
  '2019' decimal(11,2) not null,
  '2020' decimal(11,2) not null,
  primary key (`id`)
)
ENGINE = InnoDB;

drop table if exists `corti`.`tax_misc`;
create table `corti`.`tax_misc` (
  `id` integer not null auto_increment,
  `taxYear` smallint not null,
  `category` varchar(64) not null,
  `description` varchar(128) not null,
  `notesRef` varchar(128) not null,
  `amount` decimal(11,2) not null,
  primary key (`id`)
)
ENGINE = InnoDB;
```

## Some notes/details below
Read the sections below to see how to work with/load the datat

### CATEGORIES
To see all the categories
- Run updateSqlCategory, uncomment code to get list or dictionary

Insert or Delete new updateSqlCategory
- Update updateSqlCategory and run it

### Updating category 'LIVING EXPENSE' (in case want to change after initialized)
- Update spreadsheet (I had in ~/taxes/livingExpenseCategories.ods)
- Update 'updateSqlCategory.py' (at bottom) and uncomment appropriate block and ensure filename is correct

### CATEGORY REMAPPING
- Use program updateSqlRemappedCategory to insert, delete or see remapped categories, just uncomment appropriate block

### Loading SPREADSHEET Detail
- Use updateSqlWithDetail program, uncomment block so that function updateDetailDataFromSpreadsheet(yyyy) is run, you should invoke this program with the following format:
```
  python3 updateSqlWithDetail.py 2019 spreadhseetName <filename> 
```
- NOTE: It will delete the data from the detail table for the year passed in
- NOTE2: If the sheetname isn't AllDetail then pass 'sheetName <sheetName>' also

### Loading/processing the Miscellaneous Spreadsheet Data
- Use program updateSqlMisc.py, you'll see the typical commented blocks to run different routines.  Should be obvious :)

### The TAX_SUMMARY table
- NOTE: You probably need to alter the tax_summary table for the year you just processed.  I used mysql workbench to do it.  You ALSO need
        to update the mySqlSummaryTable.py program to add the new year to the array (at top of code). 

- After spreadsheets detail is loaded you want to update the tax_summary table, to do that uncomment the section in updateSqlWithSummary.py so that the appropriate section is run, it's commented pretty clearly... and is toward the bottom of the file.

- To output to spreadsheet, uncomment section in updateSqlWithSummary.py (string outputFile can be searched to see block :))

### Testing a SPREADSHEET prior to loading
- To test that the spreadsheet data is good
  - Check getSpreadsheetData.py program and turn on the conditionals as you want to test
  - Run 'python3 getSpreadsheetData spreadsheetName <filename> sheetName <sheetName)

- You should see errors to the console (if there are any)

