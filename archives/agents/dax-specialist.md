---
name: dax-specialist
description: DAX Specialist to generate and run DAX queries according to the provided model. You are able to take a query, and then according to the proposed model to run create the DAX query and to run it.
model: inherit
color: orange
---

You are a DAX Specialist for L'Oréal's Beauty Tech Data Platform (BTDP) environment.

## Schema

- path: definition/tables/DateTableTemplate_6ee25a60-95ad-4112-a624-f7a3c1e4f904.tmdl
  payload: |+
    table DateTableTemplate_6ee25a60-95ad-4112-a624-f7a3c1e4f904
    	isHidden
    	isPrivate
    	lineageTag: f397b947-9fe1-4a02-b760-bb9347c56636

    	column Date
    		dataType: dateTime
    		isHidden
    		lineageTag: e356bac3-50eb-4839-9069-2fd1f379717d
    		dataCategory: PaddedDateTableDates
    		summarizeBy: none
    		isNameInferred
    		sourceColumn: [Date]

    		annotation SummarizationSetBy = User

    	column Year = YEAR([Date])
    		dataType: int64
    		isHidden
    		lineageTag: 7caf24e5-e8a7-4f41-bea5-a60be5df2bc4
    		dataCategory: Years
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Year

    	column MonthNo = MONTH([Date])
    		dataType: int64
    		isHidden
    		lineageTag: e009cea6-77da-43be-8048-26c6418644f5
    		dataCategory: MonthOfYear
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = MonthNumber

    	column Month = FORMAT([Date], "MMMM")
    		dataType: string
    		isHidden
    		lineageTag: ceb2c3ab-51f1-4155-bd7b-275c45002cb5
    		dataCategory: Months
    		summarizeBy: none
    		sortByColumn: MonthNo

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Month

    	column QuarterNo = INT(([MonthNo] + 2) / 3)
    		dataType: int64
    		isHidden
    		lineageTag: b3312adc-71e5-4cab-b957-946dbe508f4d
    		dataCategory: QuarterOfYear
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = QuarterNumber

    	column Quarter = "Qtr " & [QuarterNo]
    		dataType: string
    		isHidden
    		lineageTag: db071771-987d-4523-8006-58b5b3b2b490
    		dataCategory: Quarters
    		summarizeBy: none
    		sortByColumn: QuarterNo

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Quarter

    	column Day = DAY([Date])
    		dataType: int64
    		isHidden
    		lineageTag: b38ae83a-2b4d-4ace-921b-b7384c80a120
    		dataCategory: DayOfMonth
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Day

    	hierarchy 'Date Hierarchy'
    		lineageTag: b5bb7b43-c5cf-47d7-a7bd-831e1042e7f1

    		level Year
    			lineageTag: 64843166-7ee7-49a2-8813-c41d2b58eac4
    			column: Year

    		level Quarter
    			lineageTag: 9eaeef8c-302a-4a58-8f00-036bd2b8712b
    			column: Quarter

    		level Month
    			lineageTag: 4570fcf7-344a-4f0c-9d62-6f6679c85be7
    			column: Month

    		level Day
    			lineageTag: 569c1097-c4f4-4831-8367-6d0795ae950e
    			column: Day

    		annotation TemplateId = DateHierarchy

    	partition DateTableTemplate_6ee25a60-95ad-4112-a624-f7a3c1e4f904 = calculated
    		mode: import
    		source = Calendar(Date(2015,1,1), Date(2015,1,1))

    	annotation __PBI_TemplateDateTable = true

    	annotation DefaultItem = DateHierarchy

- path: definition/tables/Measures_.tmdl
  payload: "table Measures_\n\tlineageTag: 8266543c-5ffb-4a8b-a926-e48830de05f2\n\n\tmeasure 'MTD BLOCKED OPEN ORDERS VALUE' = ```\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[blocked_open_order_net_sales]))* ([Period]=\"MTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 8828f820-6bbf-4535-8a4f-c28d086b2bd2\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD BLOCKED OPEN ORDERS VALUE IN EUR' = ```\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[blocked_open_order_net_sales_in_eur]))* ([Period]=\"MTD\")))\n\t\t\t\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 06e47cfa-afec-4511-ae59-a33643b0d7e0\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD BLOCKED OPEN ORDERS IN UNITS' = ```\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[blocked_open_order_sold_units]))* ([Period]=\"MTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 07019792-66c1-4ef6-9524-b206d3a45183\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD UNBLOCKED OPEN ORDERS VALUE' = ```\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[unblocked_open_order_net_sales]))* ([Period]=\"MTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 9188e6e3-d6b8-44f8-bcfe-a0165ef1947f\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD UNBLOCKED OPEN ORDERS VALUE IN EURO' =\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[unblocked_open_order_net_sales_in_eur]))* ([Period]=\"MTD\")))\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: d508ad01-618c-4f36-acc7-a1bb72ceb51c\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD UNBLOCKED OPEN ORDERS IN UNITS' =\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[unblocked_open_order_sold_units]))* ([Period]=\"MTD\")))\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 3af0c54e-d1e2-4dfe-8275-0620fa5705ac\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD % IS TARGET REACHED' = ```\n\t\t\t\n\t\t\t\n\t\t\t  VAR A=CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Invoiced sales])* ([Period]=\"MTD\")))\n\t\t\t\n\t\t\t    VAR B= CALCULATE(SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[invoiced_sales_target]))* ([Period]=\"MTD\")))\n\t\t\t\n\t\t\tRETURN DIVIDE(A,B)\n\t\t\t\n\t\t\t```\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 9b44b5c8-adb5-457f-bfb5-3a941c072b8b\n\n\tmeasure 'MTD % CNS TARGET REACHED' = ```\n\t\t\t\n\t\t\t     VAR A=CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Conso net sales])* ([Period]=\"MTD\")))\n\t\t\t\n\t\t\t    VAR B= CALCULATE(SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[conso_net_sales_target]))* ([Period]=\"MTD\")))\n\t\t\t\n\t\t\tRETURN DIVIDE(A, B)\n\t\t\t\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 4077dbf0-3049-4afb-a622-c0bb8a583bbc\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total Sales' = SUM(fact_combined[total_invoiced_sales_portfolio])+SUM(fact_combined[invoiced_sales])\n\t\tformatString: 0\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: 02c0f3dc-9abb-4d51-9157-5394696ceb13\n\n\tmeasure 'YTD BLOCKED OPEN ORDERS VALUE' = ```\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[blocked_open_order_net_sales]))* ([Period]=\"YTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 5e7a0677-1cbb-4919-9a42-3f5ed591bd6d\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD BLOCKED OPEN ORDERS VALUE IN EUR' = ```\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[blocked_open_order_net_sales_in_eur]))* ([Period]=\"YTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 41716abd-6544-4962-a098-9024f7588d00\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD BLOCKED OPEN ORDERS IN UNITS' = ```\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[blocked_open_order_sold_units]))* ([Period]=\"YTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 080bb74d-d822-4716-86c3-115cbf3d4352\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD UNBLOCKED OPEN ORDERS VALUE' =\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[unblocked_open_order_net_sales]))* ([Period]=\"YTD\")))\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: fba2c3f2-3dce-468e-8c6e-9ad5cb8867ee\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD UNBLOCKED OPEN ORDERS VALUE IN EURO' =\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[unblocked_open_order_net_sales_in_eur]))* ([Period]=\"YTD\")))\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 5fa800f2-7ef0-4894-a144-424be4a123ac\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD % IS TARGET REACHED' = ```\n\t\t\t\n\t\t\t\n\t\t\t  VAR A=CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Invoiced sales])* ([Period]=\"YTD\")))\n\t\t\t\n\t\t\t    VAR B= CALCULATE(SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[invoiced_sales_target]))* ([Period]=\"YTD\")))\n\t\t\t\n\t\t\tRETURN DIVIDE(A,B)\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t```\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: dd0ac85b-2524-4444-afe0-77b1d6136d51\n\n\tmeasure 'YTD % CNS TARGET REACHED' = ```\n\t\t\t\n\t\t\t\n\t\t\t     VAR A=CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Conso net sales])* ([Period]=\"YTD\")))\n\t\t\t\n\t\t\t    VAR B= CALCULATE(SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[conso_net_sales_target]))* ([Period]=\"YTD\")))\n\t\t\t\n\t\t\tRETURN DIVIDE(A, B)\n\t\t\t```\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 44854d99-217c-4b69-813f-774661fdf3cd\n\n\tmeasure 'Y-1 BLOCKED OPEN ORDERS VALUE IN EUR' = ```\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[blocked_open_order_net_sales_in_eur]))* ([Period]=\"Y-1\")))\n\t\t\t\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 53904ecb-83a3-4381-a14e-cd68a9f6e80a\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 BLOCKED OPEN ORDERS IN UNITS' = ```\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[blocked_open_order_sold_units]))* ([Period]=\"Y-1\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 2ee93de6-2e3f-4048-8495-e1656340222e\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 BLOCKED OPEN ORDERS VALUE' = ```\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[blocked_open_order_net_sales]))* ([Period]=\"Y-1\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: e4361220-c54b-47be-ab71-f0e718d047ce\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 UNBLOCKED OPEN ORDERS IN UNITS' =\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[unblocked_open_order_sold_units]))* ([Period]=\"Y-1\")))\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 27720d05-ea46-4776-84e4-fbd4d0231012\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 UNBLOCKED OPEN ORDERS VALUE' = ```\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[unblocked_open_order_net_sales]))* ([Period]=\"Y-1\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 719a8f24-3412-4c4a-9d75-a5943e5af2d7\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 UNBLOCKED OPEN ORDERS VALUE IN EURO' = ```\n\t\t\t\n\t\t\t  \n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[unblocked_open_order_net_sales_in_eur]))* ([Period]=\"Y-1\")))\n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 890282b1-e1ca-4db0-a4d8-ef6c81a8e49b\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 % CNS TARGET REACHED' = ```\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t     VAR A=CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Conso net sales])* ([Period]=\"Y-1\")))\n\t\t\t\n\t\t\t    VAR B= CALCULATE(SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[conso_net_sales_target]))* ([Period]=\"Y-1\")))\n\t\t\t\n\t\t\tRETURN DIVIDE(A, B)\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t```\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 40b85c2c-2604-4263-94d3-22b61ba3c6a9\n\n\tmeasure 'Y-1 % IS TARGET REACHED' = ```\n\t\t\t\n\t\t\t\n\t\t\t  VAR A=CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Invoiced sales])* ([Period]=\"Y-1\")))\n\t\t\t\n\t\t\t    VAR B= CALCULATE(SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[invoiced_sales_target]))* ([Period]=\"Y-1\")))\n\t\t\t\n\t\t\tRETURN DIVIDE(A,B)\n\t\t\t\n\t\t\t```\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: f99244ce-08e2-4bcf-90df-07ddca5a4935\n\n\tmeasure 'YOY % BLOCKED OPEN ORDERS VALUE IN EUR' =\n\t\t\t\n\t\t\tDIVIDE([YTD BLOCKED OPEN ORDERS VALUE IN EUR]-[Y-1 BLOCKED OPEN ORDERS VALUE IN EUR],[Y-1 BLOCKED OPEN ORDERS VALUE IN EUR])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: a24a9bfd-64bd-48c4-baf6-ffe4e87ad88d\n\n\tmeasure 'YOY % BLOCKED OPEN ORDERS IN UNITS' =\n\t\t\t\n\t\t\tDIVIDE([YTD BLOCKED OPEN ORDERS IN UNITS]-[Y-1 BLOCKED OPEN ORDERS IN UNITS],[Y-1 BLOCKED OPEN ORDERS IN UNITS])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 50a97f93-bfa8-4a7d-8298-aee0f11588fb\n\n\tmeasure 'YOY % UNBLOCKED OPEN ORDERS IN UNITS' =\n\t\t\t\n\t\t\tDIVIDE(\n\t\t\t[YTD UNBLOCKED OPEN ORDERS IN UNITS] -\n\t\t\t[Y-1 UNBLOCKED OPEN ORDERS IN UNITS],\n\t\t\t        [Y-1 UNBLOCKED OPEN ORDERS IN UNITS])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 2418eeaf-7f4b-479d-80f8-5dc9c69f5cf9\n\n\tmeasure 'YOY % UNBLOCKED OPEN ORDERS VALUE IN EURO' =\n\t\t\t\n\t\t\tDIVIDE(\n\t\t\t    [YTD UNBLOCKED OPEN ORDERS VALUE IN EURO]-\n\t\t\t    [Y-1 UNBLOCKED OPEN ORDERS VALUE IN EURO],\n\t\t\t    [Y-1 UNBLOCKED OPEN ORDERS VALUE IN EURO])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: c741203d-b149-43a2-b67a-bebb152bbe12\n\n\tmeasure 'YOY % UNBLOCKED OPEN ORDERS VALUE' =\n\t\t\t\n\t\t\tDIVIDE(\n\t\t\t    [YTD UNBLOCKED OPEN ORDERS VALUE] -\n\t\t\t    [Y-1 UNBLOCKED OPEN ORDERS VALUE],\n\t\t\t    [Y-1 UNBLOCKED OPEN ORDERS VALUE])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: dd1714e5-f901-4df7-b2da-00b34a7469a6\n\n\tmeasure 'YOY % IS TARGET REACHED' = ```\n\t\t\t\n\t\t\t\n\t\t\tDIVIDE([YTD % IS TARGET REACHED]-[Y-1 % IS TARGET REACHED],\n\t\t\t    [Y-1 % IS TARGET REACHED])\n\t\t\t\n\t\t\t```\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: b0502d96-9b7d-4083-b1e5-008e319e6af8\n\n\tmeasure 'YOY % CNS TARGET REACHED' =\n\t\t\t\n\t\t\tDIVIDE([YTD % CNS TARGET REACHED]-[Y-1 % CNS TARGET REACHED],\n\t\t\t        [Y-1 % CNS TARGET REACHED])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 859b7eb9-9dc6-427c-8659-8108e324db39\n\n\tmeasure 'Invoiced sales' =\n\t\t\t\n\t\t\tVAR a=\n\t\t\tSUM(fact_combined[invoiced_sales])\n\t\t\tRETURN a\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: 7c89e2da-c218-40b8-89ff-902fa442470a\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Conso net sales' =\n\t\t\t\n\t\t\tVAR A=\n\t\t\tSUM(fact_combined[conso_net_sales])\n\t\t\tRETURN A\n\t\tformatString: 0\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: b60bedf2-3ad2-480e-beb5-7c3706a6d84e\n\n\tmeasure 'Total Sales EUR' = SUM(fact_combined[total_invoiced_sales_portfolio_in_eur])+SUM(fact_combined[invoiced_sales_in_eur])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: b8aebe22-7721-4dc3-8a2f-dd02182b58bc\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD TOTAL SALES' = ```\n\t\t\t\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total Sales])* ([Period]=\"MTD\")))\n\t\t\t \n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 653a859f-ba8c-4dfc-babc-5a370ee09f3b\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD TOTAL SALES in EUR' =\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total Sales EUR])* ([Period]=\"MTD\")))\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 5c5e39c4-648b-4367-95cd-0709cf726e02\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD TOTAL SALES' = ```\n\t\t\t\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total Sales])* ([Period]=\"YTD\")))\n\t\t\t```\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: d6f3edec-3e4f-4540-8353-68fd9daeba4e\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD TOTAL SALES IN EUR' = ```\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total Sales EUR])* ([Period]=\"YTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: a8cbf08e-2b49-4b64-ba6c-b2c5046b4e74\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 TOTAL SALES' = ```\n\t\t\t\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total Sales])* ([Period]=\"Y-1\")))\n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 78ec0edd-aa99-43c8-8ad2-80256ebb5483\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 TOTAL SALES in EUR' =\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total Sales EUR])* ([Period]=\"Y-1\")))\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 520b13fe-464e-4d07-9ca5-d768978996f3\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YOY % TOTAL SALES' =\n\t\t\t\n\t\t\tDIVIDE([YTD TOTAL SALES]-[Y-1 TOTAL SALES],[Y-1 TOTAL SALES])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 1ef3bf9c-d343-4add-ac70-0921b2546e96\n\n\tmeasure 'YOY % TOTAL SALES IN EUR' =\n\t\t\t\n\t\t\tDIVIDE([YTD TOTAL SALES IN EUR]-[Y-1 TOTAL SALES in EUR],[Y-1 TOTAL SALES in EUR])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: baf3f8f5-64e2-4878-a7bd-988a8f454d2b\n\n\tmeasure 'YTD UNBLOCKED OPEN ORDERS IN UNITS' =\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE(SUM(fact_combined[unblocked_open_order_sold_units]))* ([Period]=\"YTD\")))\n\t\tformatString: 0\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: a8ff12a6-c230-4502-ab0a-883ead4365a9\n\n\tmeasure 'YOY % BLOCKED OPEN ORDERS VALUE' =\n\t\t\t\n\t\t\tDIVIDE(\n\t\t\t    [YTD BLOCKED OPEN ORDERS VALUE] -\n\t\t\t    [Y-1 BLOCKED OPEN ORDERS VALUE],\n\t\t\t    [Y-1 BLOCKED OPEN ORDERS VALUE])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 5da0f612-31d2-4234-874d-64afb893cc57\n\n\tmeasure 'Conso net sales in EUR' = SUM(fact_combined[conso_net_sales_in_eur])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: 9cd7b903-0190-4988-93e0-bc5458ae42eb\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Invoiced sales in EUR' =\n\t\t\t\n\t\t\tSUM(fact_combined[invoiced_sales_in_eur])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: 816cba1c-aac3-46ec-8647-fa31f0aef127\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Filter Date' =\n\t\t\tvar min_date =MIN(TI_Table[data_analysis])\n\t\t\tvar max_date =MAX(TI_Table[data_analysis])\n\t\t\treturn \"Date From\" & \" \" & min_date & \" \" & \"to\" &\" \" & max_date\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: 1b4ca84d-4b73-47ac-a18d-9e851f4452a7\n\n\tmeasure 'Y-1 INVOICED SALES' = ```\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Invoiced sales])* ([Period]=\"Y-1\")))\n\t\t\t \n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 73ac5f9d-1137-41f4-8e0f-453f77629030\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 CONSO NET SALES' = ```\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Conso net sales])* ([Period]=\"Y-1\")))\n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: c8dcce7f-37b1-4acd-926d-6f588ff4c942\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 INVOICED SALES IN EUR' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Invoiced sales in EUR])* ([Period]=\"Y-1\")))\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: db6945ba-8044-493d-bfaf-c7cccaac9ece\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 CONSO NET SALES IN EUR' = ```\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Conso net sales in EUR])* ([Period]=\"Y-1\")))\n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 156816e0-0f37-4489-bfda-97e801fa57c9\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YOY % INVOICED SALES' =\n\t\t\t\n\t\t\tDIVIDE([YTD INVOICED SALES]-[Y-1 INVOICED SALES],[Y-1 INVOICED SALES])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 0c4aad20-77ae-4c3d-a27b-04362bd29241\n\n\tmeasure 'YTD INVOICED SALES' = ```\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Invoiced sales])* ([Period]=\"YTD\")))\n\t\t\t \n\t\t\t```\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: f4d14820-bddd-4036-97dc-fb8d83f0a56c\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD CONSO NET SALES' = ```\n\t\t\t\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Conso net sales])* ([Period]=\"YTD\")))\n\t\t\t```\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: ef34ed96-8644-47af-b52a-97454d315421\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD INVOICED SALES IN EUR' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Invoiced sales in EUR])* ([Period]=\"YTD\")))\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 7b42063a-67a3-4ba0-b516-99aef140196a\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD CONSO NET SALES IN EUR' = ```\n\t\t\t\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Conso net sales in EUR])* ([Period]=\"YTD\")))\n\t\t\t```\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 1125c3a0-c551-4fe7-a9d8-ce19eb44306d\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YOY % CONSO NET SALES' =\n\t\t\t\n\t\t\tDIVIDE([YTD CONSO NET SALES]-[Y-1 CONSO NET SALES],[Y-1 CONSO NET SALES])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: c26b305f-dc02-49e5-9ff3-b53e2b42956f\n\n\tmeasure 'YOY % CONSO NET SALES IN EUR' =\n\t\t\t\n\t\t\tDIVIDE([YTD CONSO NET SALES IN EUR]-[Y-1 CONSO NET SALES IN EUR],[Y-1 CONSO NET SALES IN EUR])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: faad51ad-25e8-44c5-bc74-818488210151\n\n\tmeasure 'YOY % INVOICED SALES IN EUR' =\n\t\t\t\n\t\t\tDIVIDE([YTD INVOICED SALES IN EUR]-[Y-1 INVOICED SALES IN EUR],[Y-1 INVOICED SALES IN EUR])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 6b35a262-f40f-4eda-a930-b3c7a1d417a5\n\n\tmeasure 'Total minorations' = SUM(fact_combined[total_minorations])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: 2d331ffd-3bbd-4877-9a7b-7074d4a28868\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total minorations in EUR' = SUM(fact_combined[total_minorations_in_eur])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: b11c6c63-2461-4e36-9469-e5e3d8777b4f\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total customers allowances' = SUM(fact_combined[total_customers_allowances])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: 74fb095e-5b27-4451-b5d3-37352bd815a1\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total customers allowances in EUR' = SUM(fact_combined[total_customers_allowances_in_eur])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: 36e79590-18eb-428d-a817-ab9e4ac618d9\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total structural discounts' = SUM(fact_combined[total_structural_discounts])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: 19316105-0219-4f29-89b8-fedb097c5046\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total structural discounts in EUR' = SUM(fact_combined[total_structural_discounts_in_eur])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: e98142ec-d4da-4848-b341-377ef8e84475\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure Clearances = SUM(fact_combined[clearances])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: 89be4acd-5f61-4501-af3e-af6e22f5e420\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Clearances in EUR' = SUM(fact_combined[clearances_in_eur])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: 4ea7386d-0185-4f79-9d0c-30ea9b34261e\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total returns' = SUM(fact_combined[total_returns])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: 010b0d4b-04fe-4af7-9b5a-89eac6007528\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'total returns in eur' = SUM(fact_combined[total_returns_in_eur])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: ec830af9-c371-42ef-8ff2-3c13a446b1db\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Commercial returns' = SUM(fact_combined[commercial_returns])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: e72d3798-2607-4f88-a301-d9b254e6b61f\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Commercial returns in EUR' = SUM(fact_combined[commercial_returns_in_eur])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: e0028893-8f19-45f1-b8da-e1aa69de2ac9\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Returns provisions' = SUM(fact_combined[returns_provisions])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: 6dcfb7ed-09da-4234-8f52-7b835630885e\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Returns provisions in EUR' = SUM(fact_combined[returns_provisions_in_eur])\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: 616b8711-8709-4550-9044-977f57668d51\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD TOTAL MINORATIONS' = ```\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total minorations])* ([Period]=\"MTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 3889609b-9c23-4abe-b658-35c89e743fda\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD TOTAL MINORATIONS IN EUR' = ```\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total minorations in EUR])* ([Period]=\"MTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: c58682af-9ddd-4e19-8ef4-b4fd5c40c066\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD TOTAL CUSTOMERS ALLOWANCES' = ```\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total customers allowances])* ([Period]=\"MTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 6247b979-4151-4e27-bf6e-10253b3f97e6\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD TOTAL CUSTOMER ALLOWANCE IN EUR' =\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total customers allowances in EUR])* ([Period]=\"MTD\")))\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: da80a342-cb43-4c46-9813-deb754ea0165\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD TOTAL STRUCTURAL DISCOUNTS' = ```\n\t\t\t\n\t\t\t \n\t\t\t \n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total structural discounts])* ([Period]=\"MTD\")))\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 3cb91c6b-9571-4d00-8546-ffc572fa0843\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD TOTAL STRUCTURAL DISCOUNTS IN EUR' = ```\n\t\t\t\n\t\t\t \n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total structural discounts in EUR])* ([Period]=\"MTD\")))\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 0fe9acee-6bb9-4fe9-a02f-c8e019a43708\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD CLEAREANCES' = ```\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Clearances])* ([Period]=\"MTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: d328fa13-9844-4bbb-9b48-874cf7e56ec4\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD CLEARANCES IN EUR' = ```\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Clearances in EUR])* ([Period]=\"MTD\")))\n\t\t\t\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 3c5fb596-abd6-49df-b76c-48fd61abfea2\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD TOTAL RETURENS' = ```\n\t\t\t\n\t\t\t \n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total returns])* ([Period]=\"MTD\")))\n\t\t\t \n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: accee367-97d9-4bee-bc17-b0ac8e4cdbec\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD TOTAL RETURENS IN EUR' = ```\n\t\t\t\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([total returns in eur])* ([Period]=\"MTD\")))\n\t\t\t \n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: fc7da459-3f49-4567-95e5-8b9f3ccd46b7\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD COMMERCIAL RETURNS' =\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Commercial returns])* ([Period]=\"MTD\")))\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 2f2a6db5-84d4-4fe5-893b-4c9fd757e5c8\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD COMMERCIAL RETURNS IN EUR' = ```\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Commercial returns in EUR])* ([Period]=\"MTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 05d4b275-77c7-4a54-948f-adf917fac129\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD RETURNS PROVISION' =\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Returns provisions])* ([Period]=\"MTD\")))\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 3f77f0ed-69db-4e7a-a432-3ff33e18649a\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'MTD RETURNS PROVISIONS IN EUR' =\n\t\t\t\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Returns provisions in EUR])* ([Period]=\"MTD\")))\n\t\tdisplayFolder: _MTD\n\t\tlineageTag: 91c7eb12-a00e-4ba6-9d57-22925c8ca863\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 TOTAL MINORATIONS' = ```\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total minorations])* ([Period]=\"Y-1\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 7e269f1e-9e8e-48c2-ae74-3c4f89eecddf\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 TOTAL MINORATIONS IN EUR' = ```\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total minorations in EUR])* ([Period]=\"Y-1\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 301f728d-0ac9-4679-99f4-61d10379a951\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 TOTAL CUSTOMERS ALLOWANCES' = ```\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total customers allowances])* ([Period]=\"Y-1\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: dd0aebca-74aa-4b8b-8e93-d4d9245228b4\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 TOTAL CUSTOMERS ALLOWANCES IN EUR' =\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total customers allowances in EUR])* ([Period]=\"Y-1\")))\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 8cfa5600-c006-477b-8163-80a30f95d8a2\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 TOTAL STRUCTURAL DISCOUNTS' =\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total structural discounts])* ([Period]=\"Y-1\")))\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 13b1f810-d2da-4a68-9b22-de77f1b4a82f\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 TOTAL STRUCTURAL DISCOUNTS IN EUR' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total structural discounts in EUR])* ([Period]=\"Y-1\")))\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 5850f657-2f0f-40b6-becd-db8732c1bbd7\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 CLEAREANCES' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Clearances])* ([Period]=\"Y-1\")))\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 9440d1b6-45a1-4bf5-a1bd-94e27b61b7fe\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 CLEAREANCES IN EUR' = ```\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Clearances in EUR])* ([Period]=\"Y-1\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 4dfa51f2-340d-4d94-bb9e-b1373c76c8c4\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 TOTAL RETURENS' = ```\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total returns])* ([Period]=\"Y-1\")))\n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 8ef87c54-2bfc-4b7d-831b-af18afef0739\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 TOTAL RETURNS IN EUR' = ```\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([total returns in eur])* ([Period]=\"Y-1\")))\n\t\t\t \n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 965b749f-0a45-4a33-a3ee-38f44dda3d5b\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 COMMERCIAL RETURNS' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Commercial returns])* ([Period]=\"Y-1\")))\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 6577f1b5-7a3f-408a-8523-fe4dd962510e\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 COMMERCIAL RETURNS IN EUR' = ```\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Commercial returns in EUR])* ([Period]=\"Y-1\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 43d0593c-1175-455e-b31b-37b922cc3e86\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 RETURNS PROVISION' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Returns provisions])* ([Period]=\"Y-1\")))\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 3a9dc882-2fd5-47ba-bab9-e782d73f74bb\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Y-1 RETURNS PROVISION IN EUR' =\n\t\t\t\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Returns provisions in EUR])* ([Period]=\"Y-1\")))\n\t\tdisplayFolder: _Y-1\n\t\tlineageTag: 9c3643d3-2426-4614-9b2c-7202c9e45c9a\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD TOTAL MINORATIONS' = ```\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total minorations])* ([Period]=\"YTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: bd80d75c-eeb5-4223-929b-2577ebc0bfd3\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD TOTAL MINORATIONS IN EUR' = CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total minorations in EUR])* ([Period]=\"YTD\")))\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: e06e731f-138f-463b-b11d-81cab04c8730\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD TOTAL CUSTOMER ALLOWANCES' = ```\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total customers allowances])* ([Period]=\"YTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 2d08efa6-1366-44dd-ba74-976279eb81bc\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD TOTAL CUSTOMER ALLOWANCES IN EUR' = CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total customers allowances in EUR])* ([Period]=\"YTD\")))\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 3043dc17-c193-4779-8135-aadd68b5a5c5\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD TOTAL STRUCTURAL DISCOUNTS' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total structural discounts])* ([Period]=\"YTD\")))\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 3d7c43b1-a57b-4267-9fb3-ffde986ac7be\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD TOTAL STRUCTURAL DISCOUNTS IN EUR' = CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total structural discounts in EUR])* ([Period]=\"YTD\")))\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: bebe3ca3-9d88-4f83-9ba0-db2ed991590e\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD CLEAREANCES' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Clearances])* ([Period]=\"YTD\")))\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 60f74090-ab74-4ab1-9075-4954f9219ab8\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD CLEAREANCES IN EUR' = ```\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Clearances in EUR])* ([Period]=\"YTD\")))\n\t\t\t\n\t\t\t```\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: d60ea6a4-d737-412f-86b2-f1fab951318e\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD TOTAL RETURENS' = ```\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total returns])* ([Period]=\"YTD\")))\n\t\t\t```\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: aa27979a-286a-4ccb-9f91-2c60db26c145\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD TOTAL RETURENS IN EUR' = ```\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([total returns in eur])* ([Period]=\"YTD\")))\n\t\t\t```\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 0c4121b5-143c-4aa2-a285-3ab609e9a7b5\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD COMMERCIAL RETURNS' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Commercial returns])* ([Period]=\"YTD\")))\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 30502752-3b03-4aef-952c-7582be6d6564\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD COMMERCIAL RETURNS IN EUR' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Commercial returns in EUR])* ([Period]=\"Y-1\")))\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 1dd03345-bf6b-4d1f-8018-a22f96023d0b\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD RETURNS PROVISION' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Returns provisions])* ([Period]=\"YTD\")))\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: d7ccd388-bd66-43ab-9c74-b372f2edb4a8\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YTD RETURNS PROVISION IN EUR' = CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Returns provisions in EUR])* ([Period]=\"YTD\")))\n\t\tdisplayFolder: _YTD\n\t\tlineageTag: 52da1cf7-6b39-4c57-82ad-00d8f50940fd\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'YOY % TOTAL MINORATIONS' =\n\t\t\tDIVIDE( [YTD TOTAL MINORATIONS]-[Y-1 TOTAL MINORATIONS],\n\t\t\t[Y-1 TOTAL MINORATIONS])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 6c891051-9b58-48b0-be79-c794dd09f4f1\n\n\tmeasure 'YOY % TOTAL MINORATIONS in EUR' =\n\t\t\t\n\t\t\tDIVIDE( [YTD TOTAL MINORATIONS IN EUR]-[Y-1 TOTAL MINORATIONS IN EUR],\n\t\t\t[Y-1 TOTAL MINORATIONS IN EUR])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 12de5f2f-2e59-4713-a3a2-2b0749747dc6\n\n\tmeasure 'YOY % TOTAL CUSTOMER ALLOWANCES' = ```\n\t\t\t\n\t\t\t DIVIDE( [YTD TOTAL CUSTOMER ALLOWANCES]-\n\t\t\t[Y-1 TOTAL CUSTOMERS ALLOWANCES],\n\t\t\t[Y-1 TOTAL CUSTOMERS ALLOWANCES])\n\t\t\t```\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 821c5461-638d-49c1-9a81-061fa6271c79\n\n\tmeasure 'YOY % TOTAL CUSTOMER ALLOWANCES IN EUR' = ```\n\t\t\t\n\t\t\t DIVIDE( [YTD TOTAL CUSTOMER ALLOWANCES IN EUR]-\n\t\t\t[Y-1 TOTAL CUSTOMERS ALLOWANCES IN EUR],\n\t\t\t[Y-1 TOTAL CUSTOMERS ALLOWANCES IN EUR])\n\t\t\t```\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 039755a6-4760-4592-8faa-e49fe2d0ed41\n\n\tmeasure 'YOY % TOTAL STRUCTURAL DISCOUNTS' = ```\n\t\t\t\n\t\t\t DIVIDE( [YTD TOTAL STRUCTURAL DISCOUNTS]-\n\t\t\t[Y-1 TOTAL STRUCTURAL DISCOUNTS],\n\t\t\t[Y-1 TOTAL STRUCTURAL DISCOUNTS])\n\t\t\t```\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 5765e6b1-7184-431a-bf14-efaf6749b950\n\n\tmeasure 'YOY % TOTAL STRUCTURAL DISCOUNTS IN EUR' = ```\n\t\t\t\n\t\t\t DIVIDE( [YTD TOTAL STRUCTURAL DISCOUNTS IN EUR]-\n\t\t\t[Y-1 TOTAL STRUCTURAL DISCOUNTS IN EUR],\n\t\t\t[Y-1 TOTAL STRUCTURAL DISCOUNTS IN EUR])\n\t\t\t```\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 89430582-7d68-46d9-9dfe-9812bebf6f7c\n\n\tmeasure 'YOY % CLEAREANCES' = DIVIDE([YTD CLEAREANCES]-[Y-1 CLEAREANCES],[Y-1 CLEAREANCES])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 10f6599b-bd4c-462f-9eb8-44e04a17c911\n\n\tmeasure 'YOY % CLEAREANCES IN EUR' = DIVIDE([YTD CLEAREANCES IN EUR]-[Y-1 CLEAREANCES IN EUR],[Y-1 CLEAREANCES IN EUR])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: c29cd7c2-f42c-4335-82ef-91ae218ef8cf\n\n\tmeasure 'YOY % TOTAL RETURENS' = DIVIDE([YTD TOTAL RETURENS]-[Y-1 TOTAL RETURENS],[Y-1 TOTAL RETURENS])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 3b0b9e34-d7e0-400c-98e4-eecad339be1e\n\n\tmeasure 'YOY % TOTAL RETURENS IN EUR' = DIVIDE([YTD TOTAL RETURENS IN EUR]-[Y-1 TOTAL RETURNS IN EUR],[Y-1 TOTAL RETURNS IN EUR])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 59b4eaca-db85-4652-a31b-b486f116c49a\n\n\tmeasure 'YOY % COMMERCIAL RETURNS' = ```\n\t\t\t\n\t\t\tDIVIDE([YTD COMMERCIAL RETURNS]-[Y-1 COMMERCIAL RETURNS],[Y-1 COMMERCIAL RETURNS])\n\t\t\t\n\t\t\t```\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: a1db259c-eb94-416d-81fd-8386e22247c9\n\n\tmeasure 'YOY % COMMERCIAL RETURNS IN EUR' = ```\n\t\t\t\n\t\t\tDIVIDE([YTD COMMERCIAL RETURNS IN EUR]-[Y-1 COMMERCIAL RETURNS IN EUR],[Y-1 COMMERCIAL RETURNS IN EUR])\n\t\t\t\n\t\t\t```\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: bf44bee1-0bfb-4fdd-a2e6-804eed522adc\n\n\tmeasure 'YOY % RETURNS PROVISION' = DIVIDE([YTD RETURNS PROVISION]-[Y-1 RETURNS PROVISION],[Y-1 RETURNS PROVISION])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 2252ec37-1b65-4851-a882-f73f0bfa05b5\n\n\tmeasure 'YOY % RETURNS PROVISION IN EUR' = DIVIDE([YTD RETURNS PROVISION IN EUR]-[Y-1 RETURNS PROVISION IN EUR],[Y-1 RETURNS PROVISION IN EUR])\n\t\tformatString: 0.00%;-0.00%;0.00%\n\t\tdisplayFolder: _YOY\n\t\tlineageTag: 3bd76ee0-2a1c-4a57-a9b7-0746115b0af4\n\n\tmeasure 'Total Sales N' = ```\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total Sales])* ([Period]=\"N\")))\n\t\t\t```\n\t\tdisplayFolder: _N\n\t\tlineageTag: eff0be5a-cb00-4b9a-b7fe-fa538857f46f\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Clearances N' = ```\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Clearances])* ([Period]=\"N\")))\n\t\t\t```\n\t\tdisplayFolder: _N\n\t\tlineageTag: 653b91de-709f-48bd-aaa6-a867d2c2445c\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Clearances in EUR N' = ```\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Clearances in EUR])* ([Period]=\"N\")))\n\t\t\t```\n\t\tdisplayFolder: _N\n\t\tlineageTag: fdc3641f-4dcf-4726-bd39-e486aa48bd3a\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Commercial returns N' = ```\n\t\t\t\n\t\t\t \n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Commercial returns])* ([Period]=\"N\")))\n\t\t\t```\n\t\tdisplayFolder: _N\n\t\tlineageTag: a68b3cb0-97ac-47df-98c5-2d8136559ec5\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Commercial returns in EUR N' = ```\n\t\t\t\n\t\t\t \n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Commercial returns in EUR])* ([Period]=\"N\")))\n\t\t\t```\n\t\tdisplayFolder: _N\n\t\tlineageTag: 6e755b1c-c447-4139-84c8-272ecd35100c\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Conso net sales N' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Conso net sales])* ([Period]=\"N\")))\n\t\tdisplayFolder: _N\n\t\tlineageTag: 4a72624c-32f7-4932-92b1-2e9550197b56\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Conso net sales in EUR N' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Conso net sales in EUR])* ([Period]=\"N\")))\n\t\tdisplayFolder: _N\n\t\tlineageTag: 562962a9-f4dc-4acf-a86f-d170226bd571\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Invoiced sales N' = ```\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Invoiced sales])* ([Period]=\"N\")))\n\t\t\t```\n\t\tdisplayFolder: _N\n\t\tlineageTag: 37c2dfdb-74c6-45dc-95fd-22ec23a2a1d5\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Invoiced sales in EUR N' = ```\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Invoiced sales in EUR])* ([Period]=\"N\")))\n\t\t\t```\n\t\tdisplayFolder: _N\n\t\tlineageTag: 8c681d40-66b7-4b79-a31b-678f45ad18ee\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Returns provisions N' = CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Returns provisions])* ([Period]=\"N\")))\n\t\tdisplayFolder: _N\n\t\tlineageTag: 713f9bc3-438c-41af-b4d6-2a2c4cd79409\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Returns provisions in EUR N' = CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Returns provisions in EUR])* ([Period]=\"N\")))\n\t\tdisplayFolder: _N\n\t\tlineageTag: 798f7b92-4d5e-4622-9f50-a97d63a5c8c2\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total customers allowances N' = CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total customers allowances])* ([Period]=\"N\")))\n\t\tdisplayFolder: _N\n\t\tlineageTag: 0468dc19-60ec-4cae-a72c-3af635ec90bf\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total customers allowances in EUR N' = CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total customers allowances in EUR])* ([Period]=\"N\")))\n\t\tdisplayFolder: _N\n\t\tlineageTag: 447059fc-e04c-4867-8a27-00e309d95c2c\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total minorations N' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total minorations])* ([Period]=\"N\")))\n\t\tdisplayFolder: _N\n\t\tlineageTag: ea4527f9-0a53-43f3-90c5-5eb7d25aca10\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total minorationsin EUR N' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total minorations in EUR])* ([Period]=\"N\")))\n\t\tdisplayFolder: _N\n\t\tlineageTag: c8b478a8-ff70-4a51-a87d-63954f97d010\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total returns N' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total returns])* ([Period]=\"N\")))\n\t\tdisplayFolder: _N\n\t\tlineageTag: f2a29eed-9397-4722-9355-dd0d2c1371a5\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total returns in EUR N' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([total returns in eur])* ([Period]=\"N\")))\n\t\tdisplayFolder: _N\n\t\tlineageTag: b31f07df-f2b0-48ee-a58a-c9bde0bc931e\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total Sales in EUR N' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total Sales EUR])* ([Period]=\"N\")))\n\t\tdisplayFolder: _N\n\t\tlineageTag: b4317296-ce45-4733-9596-129fcd97f76b\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total structural discounts N' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total structural discounts])* ([Period]=\"N\")))\n\t\tdisplayFolder: _N\n\t\tlineageTag: 15273e52-a092-40aa-85df-2d07bf9f0b4a\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Total structural discounts in EUR N' =\n\t\t\t\n\t\t\tCALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Total structural discounts in EUR])* ([Period]=\"N\")))\n\t\tdisplayFolder: _N\n\t\tlineageTag: 6945c1d7-b826-43f8-93bc-bfd7e9d337a0\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Invoiced sales target' =\n\t\t\t\n\t\t\tVAR a=\n\t\t\tSUM(fact_combined[invoiced_sales_target])\n\t\t\tRETURN a\n\t\tdisplayFolder: _Basic\n\t\tlineageTag: de4b0b0d-def2-4807-bbae-fc116efa6c7f\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tmeasure 'Invoiced sales target N' = ```\n\t\t\t\n\t\t\t CALCULATE( SUMX(ALL(TI_Table[Period]),CALCULATE([Invoiced sales target])* ([Period]=\"N\")))\n\t\t\t```\n\t\tdisplayFolder: _N\n\t\tlineageTag: be10f5e1-4e53-4bac-8285-1e638b07f2fb\n\n\t\tannotation PBI_FormatHint = {\"isGeneralNumber\":true}\n\n\tcolumn Column\n\t\tisHidden\n\t\tformatString: 0\n\t\tlineageTag: 8af0b39b-352f-4382-9df4-495e566a39b9\n\t\tsummarizeBy: sum\n\t\tisNameInferred\n\t\tsourceColumn: [Column]\n\n\t\tannotation SummarizationSetBy = Automatic\n\n\tpartition Measures_ = calculated\n\t\tmode: import\n\t\tsource = Row(\"Column\", BLANK())\n\n\tannotation PBI_Id = ea41057e4ac54969a76ef921d3212ef5\n\n\tannotation 436ba87b-9c83-4389-a31b-ebd06a36be98 = {\"Expression\":\"\"}\n\n"
- path: definition/tables/Date.tmdl
  payload: |+
    table Date
    	lineageTag: 79b81549-b4ea-45e1-8fcb-c3bcd50d16b8

    	column Date
    		formatString: Short Date
    		lineageTag: 3660e37a-815c-4885-b1ef-75f4b5aaa6fd
    		summarizeBy: none
    		isNameInferred
    		sourceColumn: [Date]

    		variation Variation
    			isDefault
    			relationship: cf45b04a-7fb1-4e6e-a716-950afe3e6832
    			defaultHierarchy: LocalDateTable_bc1da608-328f-482f-89bd-aa0b143b50f1.'Date Hierarchy'

    		annotation SummarizationSetBy = Automatic

    	column Year
    		formatString: 0
    		lineageTag: 1a98326d-0752-45b7-8181-453a1802ff53
    		summarizeBy: sum
    		isNameInferred
    		sourceColumn: [Year]

    		annotation SummarizationSetBy = Automatic

    	column 'Month Name'
    		lineageTag: cf3aaca7-fc17-4b35-a5cd-f2584626f951
    		summarizeBy: none
    		isNameInferred
    		sourceColumn: [Month Name]

    		annotation SummarizationSetBy = Automatic

    	column 'Month Number'
    		formatString: 0
    		lineageTag: 7b046d3d-4750-46ed-83fb-8ef13f32128b
    		summarizeBy: sum
    		isNameInferred
    		sourceColumn: [Month Number]

    		annotation SummarizationSetBy = Automatic

    	column 'Week Day'
    		lineageTag: 20d3bd27-afe0-451d-87bb-919837019b13
    		summarizeBy: none
    		isNameInferred
    		sourceColumn: [Week Day]

    		annotation SummarizationSetBy = Automatic

    	column 'IsWorkingDay '
    		formatString: """TRUE"";""TRUE"";""FALSE"""
    		lineageTag: 93c635f2-778e-471c-ae37-9e5ae971f256
    		summarizeBy: none
    		isNameInferred
    		sourceColumn: [IsWorkingDay ]

    		annotation SummarizationSetBy = Automatic

    	column 'Weekday number'
    		formatString: 0
    		lineageTag: 8e609965-d846-46d0-9b76-97b2a6d4d4e6
    		summarizeBy: sum
    		isNameInferred
    		sourceColumn: [Weekday number]

    		annotation SummarizationSetBy = Automatic

    	column Quarter
    		lineageTag: c70485e0-54d6-4f58-abad-2c09aad92eb9
    		summarizeBy: none
    		isNameInferred
    		sourceColumn: [Quarter]

    		annotation SummarizationSetBy = Automatic

    	column 'Year - month'
    		lineageTag: 7e4a715b-71d9-4b9a-8de2-2a607278c39c
    		summarizeBy: none
    		isNameInferred
    		sourceColumn: [Year - month]

    		annotation SummarizationSetBy = Automatic

    	column DateAsInteger
    		lineageTag: f6564053-dd28-4999-83d3-aadccf8e4a26
    		summarizeBy: none
    		isNameInferred
    		sourceColumn: [DateAsInteger]

    		annotation SummarizationSetBy = Automatic

    	column DayOfWeekShort
    		lineageTag: 9006c89a-3d6f-4fc9-9199-cc747b742ace
    		summarizeBy: none
    		isNameInferred
    		sourceColumn: [DayOfWeekShort]

    		annotation SummarizationSetBy = Automatic

    	column MonthNameShort
    		lineageTag: b5e7bd17-c6a3-4258-942b-6adf9f7b4d4e
    		summarizeBy: none
    		isNameInferred
    		sourceColumn: [MonthNameShort]

    		annotation SummarizationSetBy = Automatic

    	partition Date = calculated
    		mode: import
    		source =
    				
    				ADDCOLUMNS (
    				CALENDAR (DATE(2019,1,1), DATE(2025,12,31)),
    				"Year", YEAR ( [Date] ),
    				"Month Name", FORMAT ( [Date], "mmmm" ),
    				"Month Number", MONTH ( [Date] ),
    				"Week Day", FORMAT([Date], "dddd") ,
    				"IsWorkingDay " ,NOT WEEKDAY( [Date]) IN { 1,7 },
    				"Weekday number", WEEKDAY( [Date],2 ),
    				"Quarter", Year([Date]) & "-Q" & Format([Date], "q"),
    				"Year - month" , Format([Date], "yyyy-mm"),
    				"DateAsInteger", FORMAT ( [Date], "YYYYMMDD" ),
    				"DayOfWeekShort", FORMAT ( [Date], "ddd" ),
    				"MonthNameShort", FORMAT ( [Date], "mmm" )
    				)

    	annotation PBI_Id = 7f3c47ec3531492288a96f4ca022ff8f

- path: definition/tables/LocalDateTable_bc1da608-328f-482f-89bd-aa0b143b50f1.tmdl
  payload: |+
    table LocalDateTable_bc1da608-328f-482f-89bd-aa0b143b50f1
    	isHidden
    	showAsVariationsOnly
    	lineageTag: a8332d18-c413-4673-9eda-8ae3db15c20b

    	column Date
    		dataType: dateTime
    		isHidden
    		lineageTag: 1435c909-d17a-4553-9fa9-a3d703a4fe6c
    		dataCategory: PaddedDateTableDates
    		summarizeBy: none
    		isNameInferred
    		sourceColumn: [Date]

    		annotation SummarizationSetBy = User

    	column Year = YEAR([Date])
    		dataType: int64
    		isHidden
    		lineageTag: 98e4f6ea-28f4-4708-8d9e-3de118a2db97
    		dataCategory: Years
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Year

    	column MonthNo = MONTH([Date])
    		dataType: int64
    		isHidden
    		lineageTag: 0ce0ea01-1803-41b1-88a8-dc322b7d7512
    		dataCategory: MonthOfYear
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = MonthNumber

    	column Month = FORMAT([Date], "MMMM")
    		dataType: string
    		isHidden
    		lineageTag: 395dc526-35e5-4ed2-be13-77aae8bc786c
    		dataCategory: Months
    		summarizeBy: none
    		sortByColumn: MonthNo

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Month

    	column QuarterNo = INT(([MonthNo] + 2) / 3)
    		dataType: int64
    		isHidden
    		lineageTag: 75b57551-3dab-47c8-aa42-39265d61525b
    		dataCategory: QuarterOfYear
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = QuarterNumber

    	column Quarter = "Qtr " & [QuarterNo]
    		dataType: string
    		isHidden
    		lineageTag: 656baf57-2da8-4e34-b174-22c1d95ec13b
    		dataCategory: Quarters
    		summarizeBy: none
    		sortByColumn: QuarterNo

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Quarter

    	column Day = DAY([Date])
    		dataType: int64
    		isHidden
    		lineageTag: 2fdd99fa-bb4e-43e9-a767-983f8cc04d4f
    		dataCategory: DayOfMonth
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Day

    	hierarchy 'Date Hierarchy'
    		lineageTag: e1058470-cc2e-4576-87a9-da9ab04c4ef3

    		level Year
    			lineageTag: 5071f264-ef5f-4bec-994f-a90933c5f017
    			column: Year

    		level Quarter
    			lineageTag: f638e4ad-9977-45f2-8b0e-f25c206cf046
    			column: Quarter

    		level Month
    			lineageTag: e1ecaffb-1db9-4129-9259-799a79f19412
    			column: Month

    		level Day
    			lineageTag: fbd36f22-49dd-4d4e-be21-5abbc7cb7510
    			column: Day

    		annotation TemplateId = DateHierarchy

    	partition LocalDateTable_bc1da608-328f-482f-89bd-aa0b143b50f1 = calculated
    		mode: import
    		source = Calendar(Date(Year(MIN('Date'[Date])), 1, 1), Date(Year(MAX('Date'[Date])), 12, 31))

    	annotation __PBI_LocalDateTable = true

- path: definition/tables/dim_axis.tmdl
  payload: |+
    table dim_axis
    	lineageTag: e7174a46-d527-47b4-8aaa-f38fad0af540

    	column axis_sk
    		dataType: int64
    		isHidden
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 40664b72-7fcd-45f9-aa50-50c72efb08be
    		summarizeBy: none
    		sourceColumn: axis_sk

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column 'Axis iph code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 18becfab-cb83-4c2b-8ad8-653ca31ce3c7
    		summarizeBy: none
    		sourceColumn: Axis iph code

    		annotation SummarizationSetBy = Automatic

    	column 'Axis description'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: f6d3a403-b1a0-4381-817b-bc199646ba02
    		summarizeBy: none
    		sourceColumn: Axis description

    		annotation SummarizationSetBy = Automatic

    	partition dim_axis = m
    		mode: directQuery
    		source =
    				let
    				   Source = GoogleBigQueryAad.Database(GCP_Project, [Implementation=null, UseStorageApi=null, ConnectionTimeout=null, CommandTimeout=null, BYOID_AudienceUri=null, ProjectId=null]),
    				    GCP_Project1 = Source{[Name=GCP_Project]}[Data],
    				    GCP_DataSet = GCP_Project1{[Name=GCP_DataSet_Dim_NeoAnalytics,Kind="Schema"]}[Data],
    				    dim_axis_View = GCP_DataSet{[Name="dim_axis",Kind="Table"]}[Data],
    				    #"Renamed Columns" = Table.RenameColumns(dim_axis_View,{{"axis_iph_code", "Axis iph code"}, {"axis_description", "Axis description"}})
    				in
    				    #"Renamed Columns"

    	annotation PBI_NavigationStepName = Navigation

    	annotation PBI_ResultType = Table

- path: definition/tables/dim_product.tmdl
  payload: |+
    table dim_product
    	lineageTag: 8374c69c-0b8f-432d-8c2c-7196c849b351

    	column product_tech_unique_id
    		dataType: int64
    		isHidden
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: ab55d6f1-2e94-45fa-aee6-2868a5c50c88
    		summarizeBy: none
    		sourceColumn: product_tech_unique_id

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column product_unique_id
    		dataType: string
    		isHidden
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 79c1abaa-4559-48aa-bc04-3ac3041261fa
    		summarizeBy: none
    		sourceColumn: product_unique_id

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column system_id
    		dataType: string
    		isHidden
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 3cc9c750-a0bf-4bca-9bba-489c0acf7e07
    		summarizeBy: none
    		sourceColumn: system_id

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column 'Product code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: f2df88f1-f30a-4bdf-a961-23b361bc1c18
    		summarizeBy: none
    		sourceColumn: Product code

    		annotation SummarizationSetBy = Automatic

    	column 'Product description'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 4430c71b-0ea1-4cb3-be87-7772ae08e18d
    		summarizeBy: none
    		sourceColumn: Product description

    		annotation SummarizationSetBy = Automatic

    	column 'Compass code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 1b021b74-2811-4ad3-90ef-d4e514acabce
    		summarizeBy: none
    		sourceColumn: Compass code

    		annotation SummarizationSetBy = Automatic

    	column 'Compass product label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 7f8d062f-80e1-41ba-81d0-f064999c4244
    		summarizeBy: none
    		sourceColumn: Compass product label

    		annotation SummarizationSetBy = Automatic

    	column 'Compass product marketing label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: e970d2a8-1829-47b9-b19e-7d6440cc19aa
    		summarizeBy: none
    		sourceColumn: Compass product marketing label

    		annotation SummarizationSetBy = Automatic

    	column 'Product gtin'
    		dataType: string
    		isHidden
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 627c1db5-73c1-404a-aaf1-93a544f5cc4d
    		summarizeBy: none
    		sourceColumn: Product gtin

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column 'Product class'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 1b599dd4-ba78-42c8-9c69-d22a25103cc4
    		summarizeBy: none
    		sourceColumn: Product class

    		annotation SummarizationSetBy = Automatic

    	column 'Product class label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: a6aaf42f-5cf8-470a-bef9-132bda9ef421
    		summarizeBy: none
    		sourceColumn: Product class label

    		annotation SummarizationSetBy = Automatic

    	column 'Product group code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 0dfecbbb-9aee-4899-9e11-6ce460b8648d
    		summarizeBy: none
    		sourceColumn: Product group code

    		annotation SummarizationSetBy = Automatic

    	column 'Product group label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 8ca0efc3-601b-4b42-a839-30d82e5590ef
    		summarizeBy: none
    		sourceColumn: Product group label

    		annotation SummarizationSetBy = Automatic

    	column 'Product category'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 68f5a96f-6026-422a-a5ca-606044764808
    		summarizeBy: none
    		sourceColumn: Product category

    		annotation SummarizationSetBy = Automatic

    	column 'Product category label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 1982e9fd-1541-4c72-b7f6-7d73c0037f4e
    		summarizeBy: none
    		sourceColumn: Product category label

    		annotation SummarizationSetBy = Automatic

    	column 'Is hero sku'
    		dataType: boolean
    		formatString: """TRUE"";""TRUE"";""FALSE"""
    		sourceProviderType: bit
    		lineageTag: d45b4583-89d1-47d5-be3b-ca8369535e30
    		summarizeBy: none
    		sourceColumn: Is hero sku

    		annotation SummarizationSetBy = Automatic

    	column 'Is promotional product'
    		dataType: boolean
    		formatString: """TRUE"";""TRUE"";""FALSE"""
    		sourceProviderType: bit
    		lineageTag: af1e0b63-d795-41d6-904d-0b9cc5f3377e
    		summarizeBy: none
    		sourceColumn: Is promotional product

    		annotation SummarizationSetBy = Automatic

    	column 'Is one shot'
    		dataType: boolean
    		formatString: """TRUE"";""TRUE"";""FALSE"""
    		sourceProviderType: bit
    		lineageTag: 9975c100-3cbf-475c-b45a-9e9d0fa0e9df
    		summarizeBy: none
    		sourceColumn: Is one shot

    		annotation SummarizationSetBy = Automatic

    	column 'Group division'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 54d7544e-daee-4a23-b3f3-f62b21e41e23
    		summarizeBy: none
    		sourceColumn: Group division

    		annotation SummarizationSetBy = Automatic

    	column 'Signature code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: dc25b1e2-85f5-49a8-a45a-e29373080ceb
    		summarizeBy: none
    		sourceColumn: Signature code

    		annotation SummarizationSetBy = Automatic

    	column 'Brand code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: f742c104-3086-45b0-912f-ec5ffc40fa16
    		summarizeBy: none
    		sourceColumn: Brand code

    		annotation SummarizationSetBy = Automatic

    	column 'Brand label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 8bd915fe-4e39-444d-8125-59e94f120d61
    		summarizeBy: none
    		sourceColumn: Brand label

    		annotation SummarizationSetBy = Automatic

    	column 'Sub brand code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 52d9c846-3b9d-4765-9cc4-fa41b8d27f8e
    		summarizeBy: none
    		sourceColumn: Sub brand code

    		annotation SummarizationSetBy = Automatic

    	column 'Sub brand label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 3bca0337-4a09-411f-a22d-20dc8fb3a114
    		summarizeBy: none
    		sourceColumn: Sub brand label

    		annotation SummarizationSetBy = Automatic

    	column 'Reference code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 75c8f46c-8570-42e3-bff1-d830fc033781
    		summarizeBy: none
    		sourceColumn: Reference code

    		annotation SummarizationSetBy = Automatic

    	column 'Reference label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 97262033-0d3e-4399-8a69-f4d5024609fd
    		summarizeBy: none
    		sourceColumn: Reference label

    		annotation SummarizationSetBy = Automatic

    	column 'Axe code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 4818ff15-88f0-4893-a215-882b439b1243
    		summarizeBy: none
    		sourceColumn: Axe code

    		annotation SummarizationSetBy = Automatic

    	column 'Axe label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 0bcf4387-2f93-4ec0-b4f1-fe8b37791442
    		summarizeBy: none
    		sourceColumn: Axe label

    		annotation SummarizationSetBy = Automatic

    	column 'Sub axe code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: dc53d137-0037-4920-84a7-eefb488eefa3
    		summarizeBy: none
    		sourceColumn: Sub axe code

    		annotation SummarizationSetBy = Automatic

    	column 'Sub axe label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: a9bd6593-7531-4cab-bdbc-3f21f930c0d9
    		summarizeBy: none
    		sourceColumn: Sub axe label

    		annotation SummarizationSetBy = Automatic

    	column 'Full hierarchy code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 890425c0-948a-4c93-ac2f-21c9dc6b2f78
    		summarizeBy: none
    		sourceColumn: Full hierarchy code

    		annotation SummarizationSetBy = Automatic

    	column 'Neo hierarchy code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: b5fc721f-e17c-40d6-9b69-eceaf0b4250c
    		summarizeBy: none
    		sourceColumn: Neo hierarchy code

    		annotation SummarizationSetBy = Automatic

    	column 'Concat signature label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: bac30031-628c-43aa-a49d-8613a54835e8
    		summarizeBy: none
    		sourceColumn: Concat signature label

    		annotation SummarizationSetBy = Automatic

    	column 'Concat brand label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 9e4ec8b8-0b70-47da-bc15-3b510021d610
    		summarizeBy: none
    		sourceColumn: Concat brand label

    		annotation SummarizationSetBy = Automatic

    	column 'Concat axe label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 73afdf19-e899-4bd6-9385-837528cf2398
    		summarizeBy: none
    		sourceColumn: Concat axe label

    		annotation SummarizationSetBy = Automatic

    	column 'Concat sub axis label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 1a6b723c-a6ea-42d4-b396-e2fadc3383a8
    		summarizeBy: none
    		sourceColumn: Concat sub axis label

    		annotation SummarizationSetBy = Automatic

    	column 'Concat sub brand label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 52096e2b-75f1-487f-9fed-7cccbbcad4c4
    		summarizeBy: none
    		sourceColumn: Concat sub brand label

    		annotation SummarizationSetBy = Automatic

    	column source_system
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: f3b3f0f7-59c6-46b7-a27a-0bff4ef4ac85
    		summarizeBy: none
    		sourceColumn: source_system

    		annotation SummarizationSetBy = Automatic

    	column 'Insert timestamp'
    		dataType: dateTime
    		formatString: General Date
    		sourceProviderType: datetime2
    		lineageTag: e999819f-b8dc-4cec-b708-bcc0d8e0f1ac
    		summarizeBy: none
    		sourceColumn: Insert timestamp

    		annotation SummarizationSetBy = Automatic

    	partition dim_product = m
    		mode: directQuery
    		source =
    				let
    				    Source = GoogleBigQueryAad.Database(GCP_Project, [Implementation=null, UseStorageApi=null, ConnectionTimeout=null, CommandTimeout=null, BYOID_AudienceUri=null, ProjectId=null]),
    				    GCP_Project1 = Source{[Name=GCP_Project]}[Data],
    				    GCP_DataSet = GCP_Project1{[Name=GCP_DataSet_Dim_NeoAnalytics,Kind="Schema"]}[Data],
    				    dim_product_View = GCP_DataSet{[Name="dim_product",Kind="Table"]}[Data],
    				    #"Renamed Columns" = Table.RenameColumns(dim_product_View,{{"product_code", "Product code"}, {"product_description", "Product description"}, {"compass_code", "Compass code"}, {"compass_product_label", "Compass product label"}, {"compass_product_marketing_label", "Compass product marketing label"}, {"product_gtin", "Product gtin"}, {"product_class_label", "Product class label"}, {"product_group_code", "Product group code"}, {"product_group_label", "Product group label"}, {"product_category", "Product category"}, {"product_class", "Product class"}, {"product_category_label", "Product category label"}, {"is_hero_sku", "Is hero sku"}, {"is_promotional_product", "Is promotional product"}, {"is_one_shot", "Is one shot"}, {"group_division", "Group division"}, {"signature_code", "Signature code"}, {"brand_code", "Brand code"}, {"brand_label", "Brand label"}, {"sub_brand_code", "Sub brand code"}, {"sub_brand_label", "Sub brand label"}, {"reference_code", "Reference code"}, {"reference_label", "Reference label"}, {"axe_code", "Axe code"}, {"axe_label", "Axe label"}, {"sub_axe_code", "Sub axe code"}, {"sub_axe_label", "Sub axe label"}, {"full_hierarchy_code", "Full hierarchy code"}, {"neo_hierarchy_code", "Neo hierarchy code"}, {"concat_signature_label", "Concat signature label"}, {"concat_brand_label", "Concat brand label"}, {"concat_axe_label", "Concat axe label"}, {"concat_sub_axis_label", "Concat sub axis label"}, {"concat_sub_brand_label", "Concat sub brand label"}, {"insert_timestamp", "Insert timestamp"}})
    				in
    				    #"Renamed Columns"

    	annotation PBI_NavigationStepName = Navigation

    	annotation PBI_ResultType = Table

- path: definition/tables/dim_sales_customer.tmdl
  payload: |+
    table dim_sales_customer
    	lineageTag: d98c2636-2e18-4101-ba08-a21020b80eb8

    	column sales_customer_tech_unique_id
    		dataType: int64
    		isHidden
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 6467e0b1-0f63-4c8d-b3cd-a206b2b073f7
    		summarizeBy: none
    		sourceColumn: sales_customer_tech_unique_id

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column sales_customer_unique_id
    		dataType: string
    		isHidden
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 2503de22-b6ad-44a6-a4f8-3fe138ba97b4
    		summarizeBy: none
    		sourceColumn: sales_customer_unique_id

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column 'Current sales customer id'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 258a894e-9802-4050-9366-c0120c1c0cff
    		summarizeBy: none
    		sourceColumn: Current sales customer id

    		annotation SummarizationSetBy = Automatic

    	column system_id
    		dataType: string
    		isHidden
    		sourceProviderType: nvarchar(16384)
    		lineageTag: dc88d65d-7d23-41bf-bcd5-ab1f58796940
    		summarizeBy: none
    		sourceColumn: system_id

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column 'Customer code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 8d61496e-16ef-4348-9c0a-793235b6f1d2
    		summarizeBy: none
    		sourceColumn: Customer code

    		annotation SummarizationSetBy = Automatic

    	column Division
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 5c16d322-5069-43a0-bdc9-300a933d4bea
    		summarizeBy: none
    		sourceColumn: Division

    		annotation SummarizationSetBy = Automatic

    	column 'Division description'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: af298b41-1b73-408c-91e9-1ee8f76e7cd9
    		summarizeBy: none
    		sourceColumn: Division description

    		annotation SummarizationSetBy = Automatic

    	column 'Group division'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 17c7751d-37ad-46f3-afe1-544b04ba109d
    		summarizeBy: none
    		sourceColumn: Group division

    		annotation SummarizationSetBy = Automatic

    	column 'Distribution channel'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 1d2c1192-702f-4caf-ae4a-f2a1dfdb81eb
    		summarizeBy: none
    		sourceColumn: Distribution channel

    		annotation SummarizationSetBy = Automatic

    	column 'Sales organization'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: c729a9e4-e64e-45c4-90ab-21109ed27ca9
    		summarizeBy: none
    		sourceColumn: Sales organization

    		annotation SummarizationSetBy = Automatic

    	column 'Sales organization description'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: debf0036-3b00-44e7-9b77-b6a4f7335b35
    		summarizeBy: none
    		sourceColumn: Sales organization description

    		annotation SummarizationSetBy = Automatic

    	column sales_area_unique_id
    		dataType: string
    		isHidden
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 25a5a45e-6d64-43a4-a19d-c042d139b730
    		summarizeBy: none
    		sourceColumn: sales_area_unique_id

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column 'Current sales area id'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: a569c0a3-f5a2-4fe2-8800-a071e3c974cd
    		summarizeBy: none
    		sourceColumn: Current sales area id

    		annotation SummarizationSetBy = Automatic

    	column customer_unique_id
    		dataType: string
    		isHidden
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 168ef7ae-1fcc-4888-b959-efaf16c20217
    		summarizeBy: none
    		sourceColumn: customer_unique_id

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column 'Current customer id'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 31d574bc-c907-445d-89d1-cb44cdee6a3f
    		summarizeBy: none
    		sourceColumn: Current customer id

    		annotation SummarizationSetBy = Automatic

    	column 'Legal organization form'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: bacd6cfd-f0ab-4280-a200-f7fc3da152d2
    		summarizeBy: none
    		sourceColumn: Legal organization form

    		annotation SummarizationSetBy = Automatic

    	column 'Customer group'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 3bfd4d54-65ce-47be-87f7-ce61cfd218a4
    		summarizeBy: none
    		sourceColumn: Customer group

    		annotation SummarizationSetBy = Automatic

    	column 'Customer group description'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: b2909989-8b1a-4c74-9011-614803b3fd57
    		summarizeBy: none
    		sourceColumn: Customer group description

    		annotation SummarizationSetBy = Automatic

    	column 'Customer classification abc analysis'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: aa2415d8-ba24-48a7-a4ce-4997f6f20d92
    		summarizeBy: none
    		sourceColumn: Customer classification abc analysis

    		annotation SummarizationSetBy = Automatic

    	column 'Sales office'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: a67ca572-1a1a-4751-82de-b6d237d21293
    		summarizeBy: none
    		sourceColumn: Sales office

    		annotation SummarizationSetBy = Automatic

    	column 'Sales group'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 3a6df5df-ed34-4ef5-b94f-ea06987c7f47
    		summarizeBy: none
    		sourceColumn: Sales group

    		annotation SummarizationSetBy = Automatic

    	column 'Sales district'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: a0fc38d9-2427-4d03-adc5-c33441d40139
    		summarizeBy: none
    		sourceColumn: Sales district

    		annotation SummarizationSetBy = Automatic

    	column 'Country iso2 code'
    		dataType: string
    		isHidden
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 3cb44891-71c3-49b5-9674-b68d7228216e
    		summarizeBy: none
    		sourceColumn: Country iso2 code

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column 'Company code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 0ba96998-d228-4443-9f8a-fe7cfc6dba94
    		summarizeBy: none
    		sourceColumn: Company code

    		annotation SummarizationSetBy = Automatic

    	column 'Price group'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 94ae54ec-6b61-439a-94c0-176b7950e4c4
    		summarizeBy: none
    		sourceColumn: Price group

    		annotation SummarizationSetBy = Automatic

    	column 'Is current'
    		dataType: boolean
    		formatString: """TRUE"";""TRUE"";""FALSE"""
    		sourceProviderType: bit
    		lineageTag: 92590c90-9d39-450c-ba42-0bfb1b795712
    		summarizeBy: none
    		sourceColumn: Is current

    		annotation SummarizationSetBy = Automatic

    	column source_system
    		dataType: string
    		isHidden
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 10c9544a-cdd9-43a0-a281-f55dc3ff3b77
    		summarizeBy: none
    		sourceColumn: source_system

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column 'Insert timestamp'
    		dataType: dateTime
    		isHidden
    		formatString: General Date
    		sourceProviderType: datetime2
    		lineageTag: 76c0768f-55d9-474c-ba12-70252ffa5aba
    		summarizeBy: none
    		sourceColumn: Insert timestamp

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column 'Sales representative code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: f291da13-7e1f-493d-8fe9-510de2505625
    		summarizeBy: none
    		sourceColumn: Sales representative code

    		annotation SummarizationSetBy = Automatic

    	column 'Customer grouping'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 0dfcfc18-87e0-4bf4-977a-0bb687c44dc7
    		summarizeBy: none
    		sourceColumn: Customer grouping

    		annotation SummarizationSetBy = Automatic

    	column 'Sales area partner functions'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: a8bf5901-5599-48cb-ab12-b475434d57eb
    		summarizeBy: none
    		sourceColumn: Sales area partner functions

    		annotation SummarizationSetBy = Automatic

    	column 'Previous master record number'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 73002496-9407-41d4-9b1e-7e33ca7c6f30
    		summarizeBy: none
    		sourceColumn: Previous master record number

    		annotation SummarizationSetBy = Automatic

    	column 'Level1 customer code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 5393ad71-ddcf-41d1-b6ae-59d4924d2e32
    		summarizeBy: none
    		sourceColumn: Level1 customer code

    		annotation SummarizationSetBy = Automatic

    	column 'Level1 customer name'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: f7437c97-723e-4c72-9808-7a505fc630f4
    		summarizeBy: none
    		sourceColumn: Level1 customer name

    		annotation SummarizationSetBy = Automatic

    	column 'Level2 customer code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: a4c1b79b-89b9-4d2a-8c3d-fffde14761b6
    		summarizeBy: none
    		sourceColumn: Level2 customer code

    		annotation SummarizationSetBy = Automatic

    	column 'Level2 customer name'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 442f5162-b4f9-46e9-ba60-20f028646a89
    		summarizeBy: none
    		sourceColumn: Level2 customer name

    		annotation SummarizationSetBy = Automatic

    	column 'Level3 customer code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 295297c9-7204-419c-96ce-fa86468dac3e
    		summarizeBy: none
    		sourceColumn: Level3 customer code

    		annotation SummarizationSetBy = Automatic

    	column 'Level3 customer name'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 9a54d700-f0e5-4b08-97ca-9fa3676a8959
    		summarizeBy: none
    		sourceColumn: Level3 customer name

    		annotation SummarizationSetBy = Automatic

    	column 'Level0 customer code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: d5bbcc8c-1ca0-4086-a579-acca44a9388e
    		summarizeBy: none
    		sourceColumn: Level0 customer code

    		annotation SummarizationSetBy = Automatic

    	column 'Level0 customer name'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 84e45fed-82c8-4067-8ded-5d8ce39639d4
    		summarizeBy: none
    		sourceColumn: Level0 customer name

    		annotation SummarizationSetBy = Automatic

    	column 'Level4 customer code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 79715332-d8cb-46d9-981e-c36363ab3191
    		summarizeBy: none
    		sourceColumn: Level4 customer code

    		annotation SummarizationSetBy = Automatic

    	column 'Level4 customer name'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: f75b7307-11d6-4ce2-90f8-75f3a6b41795
    		summarizeBy: none
    		sourceColumn: Level4 customer name

    		annotation SummarizationSetBy = Automatic

    	column 'Level5 customer code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 1d5610a8-0637-4584-8a8a-dff34c0e203d
    		summarizeBy: none
    		sourceColumn: Level5 customer code

    		annotation SummarizationSetBy = Automatic

    	column 'Level5 customer name'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 6a26a998-f747-4547-b85b-724a7258add4
    		summarizeBy: none
    		sourceColumn: Level5 customer name

    		annotation SummarizationSetBy = Automatic

    	column 'Level6 customer code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: d794a833-c04e-4d3d-a658-5cc576d80414
    		summarizeBy: none
    		sourceColumn: Level6 customer code

    		annotation SummarizationSetBy = Automatic

    	column 'Level6 customer name'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 4e0fac65-ec68-4780-81dd-570b6de1fe71
    		summarizeBy: none
    		sourceColumn: Level6 customer name

    		annotation SummarizationSetBy = Automatic

    	partition dim_sales_customer = m
    		mode: directQuery
    		source =
    				let
    				    Source = GoogleBigQueryAad.Database(GCP_Project, [Implementation=null, UseStorageApi=null, ConnectionTimeout=null, CommandTimeout=null, BYOID_AudienceUri=null, ProjectId=null]),
    				    GCP_Project1 = Source{[Name=GCP_Project]}[Data],
    				    GCP_DataSet = GCP_Project1{[Name=GCP_DataSet_Dim_NeoAnalytics,Kind="Schema"]}[Data],
    				    dim_sales_customer_View = GCP_DataSet{[Name="dim_sales_customer",Kind="Table"]}[Data],
    				    #"Renamed Columns" = Table.RenameColumns(dim_sales_customer_View,{{"current_sales_customer_id", "Current sales customer id"}, {"customer_code", "Customer code"}, {"division", "Division"}, {"division_description", "Division description"}, {"group_division", "Group division"}, {"distribution_channel", "Distribution channel"}, {"sales_organization", "Sales organization"}, {"sales_organization_description", "Sales organization description"}, {"current_sales_area_id", "Current sales area id"}, {"current_customer_id", "Current customer id"}, {"legal_organization_form", "Legal organization form"}, {"customer_group", "Customer group"}, {"customer_group_description", "Customer group description"}, {"customer_classification_abc_analysis", "Customer classification abc analysis"}, {"sales_office", "Sales office"}, {"sales_group", "Sales group"}, {"sales_district", "Sales district"}, {"country_iso2_code", "Country iso2 code"}, {"company_code", "Company code"}, {"price_group", "Price group"}, {"is_current", "Is current"}, {"sales_representative_code", "Sales representative code"}, {"insert_timestamp", "Insert timestamp"}, {"customer_grouping", "Customer grouping"}, {"sales_area_partner_functions", "Sales area partner functions"}, {"previous_master_record_number", "Previous master record number"}, {"level1_customer_code", "Level1 customer code"}, {"level1_customer_name", "Level1 customer name"}, {"level2_customer_code", "Level2 customer code"}, {"level2_customer_name", "Level2 customer name"}, {"level3_customer_code", "Level3 customer code"}, {"level3_customer_name", "Level3 customer name"}, {"level0_customer_code", "Level0 customer code"}, {"level0_customer_name", "Level0 customer name"}, {"level4_customer_code", "Level4 customer code"}, {"level4_customer_name", "Level4 customer name"}, {"level5_customer_code", "Level5 customer code"}, {"level5_customer_name", "Level5 customer name"}, {"level6_customer_code", "Level6 customer code"}, {"level6_customer_name", "Level6 customer name"}})
    				in
    				    #"Renamed Columns"

    	annotation PBI_NavigationStepName = Navigation

    	annotation PBI_ResultType = Table

- path: definition/tables/dim_sales_product.tmdl
  payload: |+
    table dim_sales_product
    	lineageTag: 0b7cac6b-e33b-4281-8a0d-47735766305e

    	column product_sales_area_tech_unique_id
    		dataType: int64
    		isHidden
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: a556195b-49f8-4a2f-b271-44e60a538a3d
    		summarizeBy: none
    		sourceColumn: product_sales_area_tech_unique_id

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column current_product_sales_area_tech_fk
    		dataType: double
    		isHidden
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 0ad8e0fd-c70b-4f1b-bfce-0f607aca8447
    		summarizeBy: none
    		sourceColumn: current_product_sales_area_tech_fk

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column system_id
    		dataType: string
    		isHidden
    		sourceProviderType: nvarchar(16384)
    		lineageTag: e2fab294-cca4-40d4-b508-c193d4b3b69d
    		summarizeBy: none
    		sourceColumn: system_id

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column Division
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 810211f1-837d-4464-9518-40026e9ebee8
    		summarizeBy: none
    		sourceColumn: Division

    		annotation SummarizationSetBy = Automatic

    	column 'Distribution channel'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: ee619cf0-9f32-4955-afb1-acf51ee9d95c
    		summarizeBy: none
    		sourceColumn: Distribution channel

    		annotation SummarizationSetBy = Automatic

    	column 'Sales organization'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 104ccbaa-c85a-460a-a193-f1f0ee79a1d5
    		summarizeBy: none
    		sourceColumn: Sales organization

    		annotation SummarizationSetBy = Automatic

    	column 'Product code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 2e7ff864-8b3e-406e-8e9c-f787169cb007
    		summarizeBy: none
    		sourceColumn: Product code

    		annotation SummarizationSetBy = Automatic

    	column 'Product account assignment group'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: d1d9b8f8-9205-423d-badb-9038c811dfa2
    		summarizeBy: none
    		sourceColumn: Product account assignment group

    		annotation SummarizationSetBy = Automatic

    	column 'Product account assignment group label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 36a7b4c2-d600-41ff-893d-65376ed46baa
    		summarizeBy: none
    		sourceColumn: Product account assignment group label

    		annotation SummarizationSetBy = Automatic

    	column 'Product pricing group'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: d35a2af2-746a-4518-a69c-81e48a8bf8cb
    		summarizeBy: none
    		sourceColumn: Product pricing group

    		annotation SummarizationSetBy = Automatic

    	column 'Product pricing group label'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 672d6d65-9c19-4101-a0d4-6312383557fe
    		summarizeBy: none
    		sourceColumn: Product pricing group label

    		annotation SummarizationSetBy = Automatic

    	column 'Is current'
    		dataType: boolean
    		formatString: """TRUE"";""TRUE"";""FALSE"""
    		sourceProviderType: bit
    		lineageTag: 0accb2cf-120e-4701-b04f-a44b848025fa
    		summarizeBy: none
    		sourceColumn: Is current

    		annotation SummarizationSetBy = Automatic

    	column 'Insert timestamp'
    		dataType: dateTime
    		isHidden
    		formatString: General Date
    		sourceProviderType: datetime2
    		lineageTag: 52be1b9f-372d-4dbe-8f17-43cef37e1dc5
    		summarizeBy: none
    		sourceColumn: Insert timestamp

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column source_system
    		dataType: string
    		isHidden
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 7b967d5c-327b-4a8b-8766-268761ee87dc
    		summarizeBy: none
    		sourceColumn: source_system

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	partition dim_sales_product = m
    		mode: directQuery
    		source =
    				let
    				    Source = GoogleBigQueryAad.Database(GCP_Project, [Implementation=null, UseStorageApi=null, ConnectionTimeout=null, CommandTimeout=null, BYOID_AudienceUri=null, ProjectId=null]),
    				    GCP_Project1 = Source{[Name=GCP_Project]}[Data],
    				    GCP_DataSet = GCP_Project1{[Name=GCP_DataSet_Dim_NeoAnalytics,Kind="Schema"]}[Data],
    				    dim_sales_product_View = GCP_DataSet{[Name="dim_sales_product",Kind="Table"]}[Data],
    				    #"Renamed Columns" = Table.RenameColumns(dim_sales_product_View,{{"division", "Division"}, {"distribution_channel", "Distribution channel"}, {"sales_organization", "Sales organization"}, {"product_code", "Product code"}, {"product_account_assignment_group", "Product account assignment group"}, {"product_account_assignment_group_label", "Product account assignment group label"}, {"product_pricing_group", "Product pricing group"}, {"product_pricing_group_label", "Product pricing group label"}, {"is_current", "Is current"}, {"insert_timestamp", "Insert timestamp"}})
    				in
    				    #"Renamed Columns"

    	annotation PBI_NavigationStepName = Navigation

    	annotation PBI_ResultType = Table

- path: definition/tables/dim_signature.tmdl
  payload: |+
    table dim_signature
    	lineageTag: 528334a1-409c-4451-a2d9-0d65bee521a1

    	column signature_sk
    		dataType: int64
    		isHidden
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: c07d242f-5cd7-4bb2-816c-ae0778cf6f68
    		summarizeBy: none
    		sourceColumn: signature_sk

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	column 'Signature code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: dcea647e-4693-4335-892f-5943ce752925
    		summarizeBy: none
    		sourceColumn: Signature code

    		annotation SummarizationSetBy = Automatic

    	column 'Signature iph code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: b291f344-f32a-4d5b-a036-5535b237577b
    		summarizeBy: none
    		sourceColumn: Signature iph code

    		annotation SummarizationSetBy = Automatic

    	column 'Signature description'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: bce659ba-4119-4945-830d-f323e06002d8
    		summarizeBy: none
    		sourceColumn: Signature description

    		annotation SummarizationSetBy = Automatic

    	partition dim_signature = m
    		mode: directQuery
    		source =
    				let
    				    Source = GoogleBigQueryAad.Database(GCP_Project, [Implementation=null, UseStorageApi=null, ConnectionTimeout=null, CommandTimeout=null, BYOID_AudienceUri=null, ProjectId=null]),
    				    GCP_Project1 = Source{[Name=GCP_Project]}[Data],
    				    GCP_DataSet = GCP_Project1{[Name=GCP_DataSet_Dim_NeoAnalytics,Kind="Schema"]}[Data],
    				    dim_signature_View = GCP_DataSet{[Name="dim_signature",Kind="Table"]}[Data],
    				    #"Renamed Columns" = Table.RenameColumns(dim_signature_View,{{"signature_code", "Signature code"}, {"signature_iph_code", "Signature iph code"}, {"signature_description", "Signature description"}})
    				in
    				    #"Renamed Columns"

    	annotation PBI_NavigationStepName = Navigation

    	annotation PBI_ResultType = Table

- path: definition/tables/Dimension Selection.tmdl
  payload: "table 'Dimension Selection'\n\tlineageTag: 29fc0477-c226-4a60-957c-62cc22fa219f\n\n\tcolumn 'Dimension Selection'\n\t\tlineageTag: a0abe93e-d421-4e6e-9c41-7dcd785a736d\n\t\tsummarizeBy: none\n\t\tsourceColumn: [Value1]\n\t\tsortByColumn: 'Dimension Selection Order'\n\n\t\trelatedColumnDetails\n\t\t\tgroupByColumn: 'Dimension Selection Fields'\n\n\t\tannotation SummarizationSetBy = Automatic\n\n\tcolumn 'Dimension Selection Fields'\n\t\tisHidden\n\t\tlineageTag: e2afa472-1c6e-4157-8778-044e515e0cfc\n\t\tsummarizeBy: none\n\t\tsourceColumn: [Value2]\n\t\tsortByColumn: 'Dimension Selection Order'\n\n\t\textendedProperty ParameterMetadata =\n\t\t\t\t{\n\t\t\t\t  \"version\": 3,\n\t\t\t\t  \"kind\": 2\n\t\t\t\t}\n\n\t\tannotation SummarizationSetBy = Automatic\n\n\tcolumn 'Dimension Selection Order'\n\t\tisHidden\n\t\tformatString: 0\n\t\tlineageTag: 97924ab2-6549-41b2-966b-1ed7c41d560a\n\t\tsummarizeBy: sum\n\t\tsourceColumn: [Value3]\n\n\t\tannotation SummarizationSetBy = Automatic\n\n\tpartition 'Dimension Selection' = calculated\n\t\tmode: import\n\t\tsource = ```\n\t\t\t\t{\n\t\t\t\t    (\"Date\", NAMEOF('Date'[Date]), 0),\n\t\t\t\t    (\"Axe code\", NAMEOF('dim_product'[Axe code]), 0),\n\t\t\t\t    (\"Axe label\", NAMEOF('dim_product'[Axe label]), 1),\n\t\t\t\t    (\"Brand code\", NAMEOF('dim_product'[Brand code]), 2),\n\t\t\t\t    (\"Brand label\", NAMEOF('dim_product'[Brand label]), 3),\n\t\t\t\t    (\"Compass code\", NAMEOF('dim_product'[Compass code]), 4),\n\t\t\t\t    (\"Compass product label\", NAMEOF('dim_product'[Compass product label]), 5),\n\t\t\t\t    (\"Compass product marketing label\", NAMEOF('dim_product'[Compass product marketing label]), 6),\n\t\t\t\t    (\"Concat axe label\", NAMEOF('dim_product'[Concat axe label]), 7),\n\t\t\t\t    (\"Concat brand label\", NAMEOF('dim_product'[Concat brand label]), 8),\n\t\t\t\t    (\"Concat signature label\", NAMEOF('dim_product'[Concat signature label]), 9),\n\t\t\t\t    (\"Concat sub axis label\", NAMEOF('dim_product'[Concat sub axis label]), 10),\n\t\t\t\t    (\"Concat sub brand label\", NAMEOF('dim_product'[Concat sub brand label]), 11),\n\t\t\t\t    (\"Full hierarchy code\", NAMEOF('dim_product'[Full hierarchy code]), 12),\n\t\t\t\t    (\"Group division\", NAMEOF('dim_product'[Group division]), 13),\n\t\t\t\t    (\"Is hero sku\", NAMEOF('dim_product'[Is hero sku]), 14),\n\t\t\t\t    (\"Is one shot\", NAMEOF('dim_product'[Is one shot]), 15),\n\t\t\t\t    (\"Is promotional product\", NAMEOF('dim_product'[Is promotional product]), 16),\n\t\t\t\t    (\"Neo hierarchy code\", NAMEOF('dim_product'[Neo hierarchy code]), 17),\n\t\t\t\t    (\"Product category\", NAMEOF('dim_product'[Product category]), 18),\n\t\t\t\t    (\"Product category label\", NAMEOF('dim_product'[Product category label]), 19),\n\t\t\t\t    (\"Product class\", NAMEOF('dim_product'[Product class]), 20),\n\t\t\t\t    (\"Product class label\", NAMEOF('dim_product'[Product class label]), 21),\n\t\t\t\t    (\"Product code\", NAMEOF('dim_product'[Product code]), 22),\n\t\t\t\t    (\"Product description\", NAMEOF('dim_product'[Product description]), 23),\n\t\t\t\t    (\"Product group code\", NAMEOF('dim_product'[Product group code]), 24),\n\t\t\t\t    (\"Product group label\", NAMEOF('dim_product'[Product group label]), 25),\n\t\t\t\t    (\"Product gtin\", NAMEOF('dim_product'[Product gtin]), 26),\n\t\t\t\t    (\"Reference code\", NAMEOF('dim_product'[Reference code]), 27),\n\t\t\t\t    (\"Reference label\", NAMEOF('dim_product'[Reference label]), 28),\n\t\t\t\t    (\"Signature code\", NAMEOF('dim_product'[Signature code]), 29),\n\t\t\t\t    (\"Sub axe code\", NAMEOF('dim_product'[Sub axe code]), 30),\n\t\t\t\t    (\"Sub axe label\", NAMEOF('dim_product'[Sub axe label]), 31),\n\t\t\t\t    (\"Sub brand code\", NAMEOF('dim_product'[Sub brand code]), 32),\n\t\t\t\t    (\"Sub brand label\", NAMEOF('dim_product'[Sub brand label]), 33),\n\t\t\t\t    (\"Company code\", NAMEOF('dim_sales_customer'[Company code]), 34),\n\t\t\t\t    (\"Current customer id\", NAMEOF('dim_sales_customer'[Current customer id]), 35),\n\t\t\t\t    (\"Current sales area id\", NAMEOF('dim_sales_customer'[Current sales area id]), 36),\n\t\t\t\t    (\"Country iso2 code\", NAMEOF('dim_sales_customer'[Country iso2 code]), 37),\n\t\t\t\t    (\"Current sales customer id\", NAMEOF('dim_sales_customer'[Current sales customer id]), 38),\n\t\t\t\t    (\"Customer classification abc analysis\", NAMEOF('dim_sales_customer'[Customer classification abc analysis]), 39),\n\t\t\t\t    (\"Customer code\", NAMEOF('dim_sales_customer'[Customer code]), 40),\n\t\t\t\t    (\"Customer group\", NAMEOF('dim_sales_customer'[Customer group]), 41),\n\t\t\t\t    (\"Customer group description\", NAMEOF('dim_sales_customer'[Customer group description]), 42),\n\t\t\t\t    (\"Customer grouping\", NAMEOF('dim_sales_customer'[Customer grouping]), 43),\n\t\t\t\t    (\"Distribution channel\", NAMEOF('dim_sales_customer'[Distribution channel]), 44),\n\t\t\t\t    (\"Division\", NAMEOF('dim_sales_customer'[Division]), 45),\n\t\t\t\t    (\"Division description\", NAMEOF('dim_sales_customer'[Division description]), 46),\n\t\t\t\t    (\"Is current\", NAMEOF('dim_sales_customer'[Is current]), 47),\n\t\t\t\t    (\"Legal organization form\", NAMEOF('dim_sales_customer'[Legal organization form]), 48),\n\t\t\t\t    (\"Level0 customer code\", NAMEOF('dim_sales_customer'[Level0 customer code]), 49),\n\t\t\t\t    (\"Level0 customer name\", NAMEOF('dim_sales_customer'[Level0 customer name]), 50),\n\t\t\t\t    (\"Level1 customer code\", NAMEOF('dim_sales_customer'[Level1 customer code]), 51),\n\t\t\t\t    (\"Level1 customer name\", NAMEOF('dim_sales_customer'[Level1 customer name]), 52),\n\t\t\t\t    (\"Level2 customer code\", NAMEOF('dim_sales_customer'[Level2 customer code]), 53),\n\t\t\t\t    (\"Level2 customer name\", NAMEOF('dim_sales_customer'[Level2 customer name]), 54),\n\t\t\t\t    (\"Level3 customer code\", NAMEOF('dim_sales_customer'[Level3 customer code]), 55),\n\t\t\t\t    (\"Level3 customer name\", NAMEOF('dim_sales_customer'[Level3 customer name]), 56),\n\t\t\t\t    (\"Level4 customer code\", NAMEOF('dim_sales_customer'[Level4 customer code]), 57),\n\t\t\t\t    (\"Level4 customer name\", NAMEOF('dim_sales_customer'[Level4 customer name]), 58),\n\t\t\t\t    (\"Level5 customer code\", NAMEOF('dim_sales_customer'[Level5 customer code]), 59),\n\t\t\t\t    (\"Level5 customer name\", NAMEOF('dim_sales_customer'[Level5 customer name]), 60),\n\t\t\t\t    (\"Level6 customer code\", NAMEOF('dim_sales_customer'[Level6 customer code]), 61),\n\t\t\t\t    (\"Level6 customer name\", NAMEOF('dim_sales_customer'[Level6 customer name]), 62),\n\t\t\t\t    (\"Previous master record number\", NAMEOF('dim_sales_customer'[Previous master record number]), 63),\n\t\t\t\t    (\"Price group\", NAMEOF('dim_sales_customer'[Price group]), 64),\n\t\t\t\t    (\"Sales area partner functions\", NAMEOF('dim_sales_customer'[Sales area partner functions]), 65),\n\t\t\t\t    (\"Sales district\", NAMEOF('dim_sales_customer'[Sales district]), 66),\n\t\t\t\t    (\"Sales group\", NAMEOF('dim_sales_customer'[Sales group]), 67),\n\t\t\t\t    (\"Sales office\", NAMEOF('dim_sales_customer'[Sales office]), 68),\n\t\t\t\t    (\"Sales organization\", NAMEOF('dim_sales_customer'[Sales organization]), 69),\n\t\t\t\t    (\"Sales organization description\", NAMEOF('dim_sales_customer'[Sales organization description]), 70),\n\t\t\t\t    (\"Sales representative code\", NAMEOF('dim_sales_customer'[Sales representative code]), 71),\n\t\t\t\t    (\"Distribution channel\", NAMEOF('dim_sales_product'[Distribution channel]), 72),\n\t\t\t\t    (\"Insert timestamp\", NAMEOF('dim_sales_product'[Insert timestamp]), 73),\n\t\t\t\t    (\"Is current\", NAMEOF('dim_sales_product'[Is current]), 74),\n\t\t\t\t    (\"Product account assignment group\", NAMEOF('dim_sales_product'[Product account assignment group]), 75),\n\t\t\t\t    (\"Product account assignment group label\", NAMEOF('dim_sales_product'[Product account assignment group label]), 76),\n\t\t\t\t    (\"Product code\", NAMEOF('dim_sales_product'[Product code]), 77),\n\t\t\t\t    (\"Product pricing group\", NAMEOF('dim_sales_product'[Product pricing group]), 78),\n\t\t\t\t    (\"Product pricing group label\", NAMEOF('dim_sales_product'[Product pricing group label]), 79),\n\t\t\t\t    (\"Sales organization\", NAMEOF('dim_sales_product'[Sales organization]), 80),\n\t\t\t\t    (\"Signature code\", NAMEOF('dim_signature'[Signature code]), 81),\n\t\t\t\t    (\"Hub code\", NAMEOF(dim_hub[Hub code]), 82),\n\t\t\t\t    (\"Hub desc\", NAMEOF(dim_hub[Hub desc]), 83),\n\t\t\t\t    (\"Zone code\", NAMEOF(dim_hub[Zone code]), 84),\n\t\t\t\t    (\"Zone desc\", NAMEOF(dim_hub[Zone desc]), 85),\n\t\t\t\t    (\"Custom subbrand group\", NAMEOF(customGroup[Custom subbrand group]), 86),\n\t\t\t\t    (\"Sub brand code\", NAMEOF(customGroup[Subbrand code]), 87)\n\t\t\t\t    \n\t\t\t\t}\n\t\t\t\t```\n\n\tannotation PBI_Id = 630923d94bd34cadbe0fd77ac7d55f19\n\n"
- path: definition/tables/KPI Selection.tmdl
  payload: "table 'KPI Selection'\n\tlineageTag: c3709ce0-edb3-4704-84bc-97543d8ab4be\n\n\tcolumn 'KPI Selection'\n\t\tlineageTag: 742fdecd-1181-49a7-a0a1-127671104725\n\t\tsummarizeBy: none\n\t\tsourceColumn: [Value1]\n\t\tsortByColumn: 'KPI Selection Order'\n\n\t\trelatedColumnDetails\n\t\t\tgroupByColumn: 'KPI Selection Fields'\n\n\t\tannotation SummarizationSetBy = Automatic\n\n\tcolumn 'KPI Selection Fields'\n\t\tisHidden\n\t\tlineageTag: c13c3240-3c04-4e4b-aa14-76c6ebcab4e8\n\t\tsummarizeBy: none\n\t\tsourceColumn: [Value2]\n\t\tsortByColumn: 'KPI Selection Order'\n\n\t\textendedProperty ParameterMetadata =\n\t\t\t\t{\n\t\t\t\t  \"version\": 3,\n\t\t\t\t  \"kind\": 2\n\t\t\t\t}\n\n\t\tannotation SummarizationSetBy = Automatic\n\n\tcolumn 'KPI Selection Order'\n\t\tisHidden\n\t\tformatString: 0\n\t\tlineageTag: 14aa70cf-9488-4200-9c2a-af6743ab5e41\n\t\tsummarizeBy: sum\n\t\tsourceColumn: [Value3]\n\n\t\tannotation SummarizationSetBy = Automatic\n\n\tpartition 'KPI Selection' = calculated\n\t\tmode: import\n\t\tsource = ```\n\t\t\t\t{\n\t\t\t\t    (\"Invoiced sales\", NAMEOF('Measures_'[Invoiced sales]), 0),\n\t\t\t\t    (\"Invoiced sales Y-1 \", NAMEOF('Measures_'[Y-1 INVOICED SALES]), 1),\n\t\t\t\t    (\"% Invoiced sales vs Y-1 \", NAMEOF('Measures_'[YOY % INVOICED SALES]), 2),\n\t\t\t\t\n\t\t\t\t    (\"Invoiced sales in EUR\", NAMEOF('Measures_'[Invoiced sales in EUR]), 3),\n\t\t\t\t    (\"Invoiced sales in EUR Y-1\", NAMEOF('Measures_'[Y-1 INVOICED SALES IN EUR]), 4),\n\t\t\t\t    (\"% Invoiced sales in EUR vs Y-1\", NAMEOF('Measures_'[YOY % INVOICED SALES IN EUR]), 5),\n\t\t\t\t\n\t\t\t\t    (\"Conso net sales\", NAMEOF('Measures_'[Conso net sales]), 6),\n\t\t\t\t    (\"Conso net sales Y-1\", NAMEOF('Measures_'[Y-1 CONSO NET SALES]), 7),\n\t\t\t\t    (\"% Conso net sales vs Y-1\", NAMEOF('Measures_'[YOY % CONSO NET SALES]), 8),\n\t\t\t\t\n\t\t\t\t    (\"Conso net sales in EUR\", NAMEOF('Measures_'[Conso net sales in EUR]), 9),\n\t\t\t\t    (\"Conso net sales in EUR Y-1\", NAMEOF('Measures_'[Y-1 CONSO NET SALES IN EUR]), 10),\n\t\t\t\t    (\"% Conso net sales in EUR vs Y-1\", NAMEOF('Measures_'[YOY % CONSO NET SALES IN EUR]), 11),\n\t\t\t\t    \n\t\t\t\t    (\"Invoiced sales + Total portfolio value\", NAMEOF('Measures_'[Total Sales]), 12),\n\t\t\t\t    (\"Invoiced sales + Total portfolio value Y-1\", NAMEOF('Measures_'[Y-1 TOTAL SALES]), 13),\n\t\t\t\t    (\"% Invoiced sales + Total portfolio value\", NAMEOF('Measures_'[YOY % TOTAL SALES]), 14),\n\t\t\t\t\n\t\t\t\t    (\"Invoiced sales + Total portfolio in EUR\", NAMEOF('Measures_'[Total Sales EUR]), 15),\n\t\t\t\t    (\"Invoiced sales + Total portfolio in EUR\", NAMEOF('Measures_'[Y-1 TOTAL SALES in EUR]), 16),\n\t\t\t\t     (\"% Invoiced sales + Total portfolio in EUR\", NAMEOF('Measures_'[YOY % TOTAL SALES IN EUR]), 17),\n\t\t\t\t\n\t\t\t\t    (\"MTD % CNS Target Reached\", NAMEOF('Measures_'[MTD % CNS TARGET REACHED]), 18),\n\t\t\t\t    (\"MTD % IS Target Reached\", NAMEOF('Measures_'[MTD % IS TARGET REACHED]), 19),\n\t\t\t\t   \n\t\t\t\t    (\"Y-1 % CNS Target Reached\", NAMEOF('Measures_'[Y-1 % CNS TARGET REACHED]), 20),\n\t\t\t\t    (\"Y-1 % IS Target Reached\", NAMEOF('Measures_'[Y-1 % IS TARGET REACHED]), 21),\n\t\t\t\t    (\"Y-1 Total Sales\", NAMEOF('Measures_'[Y-1 TOTAL SALES]), 22),\n\t\t\t\t    (\"Y-1 Total Sales in EUR\", NAMEOF('Measures_'[Y-1 TOTAL SALES in EUR]), 23),\n\t\t\t\t  \n\t\t\t\t    (\"YOY % Target Reached\", NAMEOF('Measures_'[YOY % CNS TARGET REACHED]), 24),\n\t\t\t\t    (\"YOY % IS Target Reached\", NAMEOF('Measures_'[YOY % IS TARGET REACHED]), 25),\n\t\t\t\t    (\"YTD % CNS Target Reached\", NAMEOF('Measures_'[YTD % CNS TARGET REACHED]), 26),\n\t\t\t\t    (\"YTD % IS Target Reached\", NAMEOF('Measures_'[YTD % IS TARGET REACHED]), 27)\n\t\t\t\t    \n\t\t\t\t}\n\t\t\t\t```\n\n\tannotation PBI_Id = f7d90ffd8f09426bba3a608c51d80cc1\n\n"
- path: definition/tables/dim_hub.tmdl
  payload: |+
    table dim_hub
    	lineageTag: 68a37952-f812-4490-9f72-e9a3317d23c0

    	column 'Zone code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 5e2feca4-4906-4eab-b81e-850167d9898d
    		summarizeBy: none
    		sourceColumn: Zone code

    		annotation SummarizationSetBy = Automatic

    	column 'Zone desc'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 7e0a745d-1512-4092-ba57-5d22c49834b3
    		summarizeBy: none
    		sourceColumn: Zone desc

    		annotation SummarizationSetBy = Automatic

    	column 'Hub code'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 852f9399-f119-41e9-aff1-533fe8b430ce
    		summarizeBy: none
    		sourceColumn: Hub code

    		annotation SummarizationSetBy = Automatic

    	column 'Hub desc'
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: a2138466-ce31-4c75-846a-470ef5c74a1c
    		summarizeBy: none
    		sourceColumn: Hub desc

    		annotation SummarizationSetBy = Automatic

    	column hub_sk
    		dataType: int64
    		isHidden
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 9c2c825d-5aff-4ab3-b025-2070b3ff66d7
    		summarizeBy: none
    		sourceColumn: hub_sk

    		changedProperty = IsHidden

    		annotation SummarizationSetBy = Automatic

    	partition dim_hub = m
    		mode: directQuery
    		source =
    				let
    				   Source = GoogleBigQueryAad.Database(GCP_Project, [Implementation=null, UseStorageApi=null, ConnectionTimeout=null, CommandTimeout=null, BYOID_AudienceUri=null, ProjectId=null]),
    				    GCP_Project1 = Source{[Name=GCP_Project]}[Data],
    				    GCP_DataSet = GCP_Project1{[Name=GCP_DataSet_Dim_NeoAnalytics,Kind="Schema"]}[Data],
    				    dim_axis_View = GCP_DataSet{[Name="dim_hub",Kind="Table"]}[Data],
    				    #"Renamed Columns" = Table.RenameColumns(dim_axis_View,{{"zone_code", "Zone code"}, {"zone_desc", "Zone desc"}, {"hub_code", "Hub code"}, {"hub_desc", "Hub desc"}})
    				in
    				    #"Renamed Columns"

    	annotation PBI_NavigationStepName = Navigation

    	annotation PBI_ResultType = Table

- path: definition/tables/fact_combined.tmdl
  payload: |+
    table fact_combined
    	lineageTag: f9b6e5b5-a724-4c68-a760-9e1166ee9e42

    	column date
    		dataType: dateTime
    		formatString: Long Date
    		sourceProviderType: date
    		lineageTag: 628b3b0e-ce09-4082-8ea1-3b63c8191ef3
    		summarizeBy: none
    		sourceColumn: date

    		annotation SummarizationSetBy = Automatic

    		annotation UnderlyingDateTimeDataType = Date

    	column hub_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 992fe8cb-9880-4155-b6a6-ce2a584366eb
    		summarizeBy: none
    		sourceColumn: hub_code

    		annotation SummarizationSetBy = Automatic

    	column hub
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 18e9f1b8-10e2-4d91-981d-62d08756bf77
    		summarizeBy: none
    		sourceColumn: hub

    		annotation SummarizationSetBy = Automatic

    	column zone_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 7079284f-7ab5-4aab-86b7-bbd85544a658
    		summarizeBy: none
    		sourceColumn: zone_code

    		annotation SummarizationSetBy = Automatic

    	column zone
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 0e93d0c0-d98e-4bde-87f8-59a2f863d80f
    		summarizeBy: none
    		sourceColumn: zone

    		annotation SummarizationSetBy = Automatic

    	column company_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 648499b7-1d08-464a-be96-49d11e5dd797
    		summarizeBy: none
    		sourceColumn: company_code

    		annotation SummarizationSetBy = Automatic

    	column company
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 3f0400eb-43e4-4f77-acfc-8714a63030a5
    		summarizeBy: none
    		sourceColumn: company

    		annotation SummarizationSetBy = Automatic

    	column group_division
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: bc993c5d-528a-4dc6-9e8e-27bf2c9a7d3f
    		summarizeBy: none
    		sourceColumn: group_division

    		annotation SummarizationSetBy = Automatic

    	column sales_organization
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 8bb101ec-f2ed-4105-84ad-951b9f3a5ece
    		summarizeBy: none
    		sourceColumn: sales_organization

    		annotation SummarizationSetBy = Automatic

    	column division
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 95252235-dec0-4d96-8642-a3f336fbe398
    		summarizeBy: none
    		sourceColumn: division

    		annotation SummarizationSetBy = Automatic

    	column distribution_channel
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 39be0481-a010-483c-880a-df5db7b3156d
    		summarizeBy: none
    		sourceColumn: distribution_channel

    		annotation SummarizationSetBy = Automatic

    	column product_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 99b648e3-b0e3-4e01-aef5-d476554fdb53
    		summarizeBy: none
    		sourceColumn: product_code

    		annotation SummarizationSetBy = Automatic

    	column product_tech_fk
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: a5428c48-d62e-44ee-8a97-355aee1b7664
    		summarizeBy: none
    		sourceColumn: product_tech_fk

    		annotation SummarizationSetBy = Automatic

    	column product_sales_area_tech_fk
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 033927db-aa6b-4216-9afc-2d68c5c47efc
    		summarizeBy: none
    		sourceColumn: product_sales_area_tech_fk

    		annotation SummarizationSetBy = Automatic

    	column compass_product_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 4dbcdd73-22b5-43ad-a2a9-6062e08ac377
    		summarizeBy: none
    		sourceColumn: compass_product_code

    		annotation SummarizationSetBy = Automatic

    	column posted_product_gtin
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: f01f0f92-630a-46aa-9442-14268c2b260f
    		summarizeBy: none
    		sourceColumn: posted_product_gtin

    		annotation SummarizationSetBy = Automatic

    	column bom_higher_level
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: a04bc7aa-c4b1-4616-a3ec-143f6261bfc6
    		summarizeBy: none
    		sourceColumn: bom_higher_level

    		annotation SummarizationSetBy = Automatic

    	column bom_intermediate
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: e7142795-a6bc-423e-ac5e-5d6d16639d36
    		summarizeBy: none
    		sourceColumn: bom_intermediate

    		annotation SummarizationSetBy = Automatic

    	column posted_brand_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 115bad24-9a34-476d-99ae-c0c7bb28ef92
    		summarizeBy: none
    		sourceColumn: posted_brand_code

    		annotation SummarizationSetBy = Automatic

    	column posted_brand
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: a575b554-6fec-470f-9bc2-20736528e1c6
    		summarizeBy: none
    		sourceColumn: posted_brand

    		annotation SummarizationSetBy = Automatic

    	column posted_sub_brand_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: e7976b0b-2af1-4d5b-b5d2-22de15bb9003
    		summarizeBy: none
    		sourceColumn: posted_sub_brand_code

    		annotation SummarizationSetBy = Automatic

    	column posted_sub_brand
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 181a84c2-b3ad-43e5-ab45-a49edeb22441
    		summarizeBy: none
    		sourceColumn: posted_sub_brand

    		annotation SummarizationSetBy = Automatic

    	column customer_sold_to_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 0f85329b-504d-446d-a9c8-9332e95c0a6f
    		summarizeBy: none
    		sourceColumn: customer_sold_to_code

    		annotation SummarizationSetBy = Automatic

    	column customer_sold_to
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 4cd49634-89c3-4402-8de2-de529839c236
    		summarizeBy: none
    		sourceColumn: customer_sold_to

    		annotation SummarizationSetBy = Automatic

    	column sales_customer_tech_fk
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 0dcdc868-777b-4bc9-8716-4e67e5e4fb83
    		summarizeBy: none
    		sourceColumn: sales_customer_tech_fk

    		annotation SummarizationSetBy = Automatic

    	column customer_compass_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 71675c51-55b2-4335-bd25-a6fe4087f41f
    		summarizeBy: none
    		sourceColumn: customer_compass_code

    		annotation SummarizationSetBy = Automatic

    	column posted_customer_hierarchy_1_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 45b9860b-c202-4d22-bb4e-b44d02bb5fc7
    		summarizeBy: none
    		sourceColumn: posted_customer_hierarchy_1_code

    		annotation SummarizationSetBy = Automatic

    	column posted_customer_hierarchy_1
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 35707e0c-7f67-4cf8-b5ae-784442c1fa16
    		summarizeBy: none
    		sourceColumn: posted_customer_hierarchy_1

    		annotation SummarizationSetBy = Automatic

    	column posted_customer_hierarchy_2_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 29eb0fde-6139-47fa-98af-2e1456252584
    		summarizeBy: none
    		sourceColumn: posted_customer_hierarchy_2_code

    		annotation SummarizationSetBy = Automatic

    	column posted_customer_hierarchy_2
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 7617933c-1ff2-4fae-860c-9777a1183a93
    		summarizeBy: none
    		sourceColumn: posted_customer_hierarchy_2

    		annotation SummarizationSetBy = Automatic

    	column posted_customer_hierarchy_3_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 7d137eef-dad9-477f-b385-a27a6f7727e5
    		summarizeBy: none
    		sourceColumn: posted_customer_hierarchy_3_code

    		annotation SummarizationSetBy = Automatic

    	column posted_customer_hierarchy_3
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: f4551682-6fa0-456b-85e4-6a505ba73d08
    		summarizeBy: none
    		sourceColumn: posted_customer_hierarchy_3

    		annotation SummarizationSetBy = Automatic

    	column posted_customer_hierarchy_4_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 7dc4cfa7-6785-41da-bd09-3b5aa4a88c39
    		summarizeBy: none
    		sourceColumn: posted_customer_hierarchy_4_code

    		annotation SummarizationSetBy = Automatic

    	column posted_customer_hierarchy_4
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 879e437f-2a65-407c-bdbe-3b6111201b66
    		summarizeBy: none
    		sourceColumn: posted_customer_hierarchy_4

    		annotation SummarizationSetBy = Automatic

    	column posted_customer_hierarchy_5_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 01e95c90-a0dd-47c3-b656-c0d1912afc88
    		summarizeBy: none
    		sourceColumn: posted_customer_hierarchy_5_code

    		annotation SummarizationSetBy = Automatic

    	column posted_customer_hierarchy_5
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 6215753f-ce09-4e7c-b8c2-3d1855f0780d
    		summarizeBy: none
    		sourceColumn: posted_customer_hierarchy_5

    		annotation SummarizationSetBy = Automatic

    	column invoice_number
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: e08f3529-b4e8-43b7-a42b-66b3edc8ffc9
    		summarizeBy: none
    		sourceColumn: invoice_number

    		annotation SummarizationSetBy = Automatic

    	column invoice_document_type
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 0b461628-2b9a-4f88-bc32-4ab7e1f514e7
    		summarizeBy: none
    		sourceColumn: invoice_document_type

    		annotation SummarizationSetBy = Automatic

    	column sales_order_number
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 9d9cbe66-5260-44d9-bac3-8cdb9fac3817
    		summarizeBy: none
    		sourceColumn: sales_order_number

    		annotation SummarizationSetBy = Automatic

    	column posted_sales_rep
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 15ce8fa2-f76f-4954-9dcc-6d874b796af5
    		summarizeBy: none
    		sourceColumn: posted_sales_rep

    		annotation SummarizationSetBy = Automatic

    	column posted_sales_office
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 47204b2a-1de5-4d94-abbc-979ddd68b7f3
    		summarizeBy: none
    		sourceColumn: posted_sales_office

    		annotation SummarizationSetBy = Automatic

    	column posted_sales_group
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 51b62c52-b437-49d8-a0db-d2e1b5e29c20
    		summarizeBy: none
    		sourceColumn: posted_sales_group

    		annotation SummarizationSetBy = Automatic

    	column currency
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 3127fa27-f004-4a65-bbe2-5630f7d9a654
    		summarizeBy: none
    		sourceColumn: currency

    		annotation SummarizationSetBy = Automatic

    	column amaas_job_function_bitmap
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 3906cc6b-6e3e-4f1b-9a39-934e1b53140e
    		summarizeBy: sum
    		sourceColumn: amaas_job_function_bitmap

    		annotation SummarizationSetBy = Automatic

    	column amaas_signature_bitmap1
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: cbffb833-37af-492f-8b4d-a14eb16c3523
    		summarizeBy: sum
    		sourceColumn: amaas_signature_bitmap1

    		annotation SummarizationSetBy = Automatic

    	column amaas_signature_bitmap2
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 6fec6d82-98bf-4eb2-a227-47e66e0b0c03
    		summarizeBy: sum
    		sourceColumn: amaas_signature_bitmap2

    		annotation SummarizationSetBy = Automatic

    	column amaas_entity_type_bitmap
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 7b6d33ef-63d2-4e46-a5f4-962c63c26342
    		summarizeBy: sum
    		sourceColumn: amaas_entity_type_bitmap

    		annotation SummarizationSetBy = Automatic

    	column amaas_hub_bitmap1
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: bde9a055-630b-408e-a57b-b1d181add9b8
    		summarizeBy: sum
    		sourceColumn: amaas_hub_bitmap1

    		annotation SummarizationSetBy = Automatic

    	column amaas_hub_bitmap2
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: e5dc6903-5ed3-49aa-8b9d-85ac266e4a5a
    		summarizeBy: sum
    		sourceColumn: amaas_hub_bitmap2

    		annotation SummarizationSetBy = Automatic

    	column amaas_hub_bitmap3
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 640dfacb-a310-42ce-b7f1-8a6f20e6156f
    		summarizeBy: sum
    		sourceColumn: amaas_hub_bitmap3

    		annotation SummarizationSetBy = Automatic

    	column amaas_hub_bitmap4
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 4882936c-1a5b-4476-a4cb-a6ecd3d7f888
    		summarizeBy: sum
    		sourceColumn: amaas_hub_bitmap4

    		annotation SummarizationSetBy = Automatic

    	column amaas_hub_bitmap5
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 7f1781c3-5d71-4184-a218-0fc6d6d17d08
    		summarizeBy: sum
    		sourceColumn: amaas_hub_bitmap5

    		annotation SummarizationSetBy = Automatic

    	column amaas_division_bitmap
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 96dca3df-65a7-4489-81ef-bc7d45ae7bf3
    		summarizeBy: sum
    		sourceColumn: amaas_division_bitmap

    		annotation SummarizationSetBy = Automatic

    	column invoice_item_number
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 3bb3ed70-e904-4653-850f-78d91ee29a2a
    		summarizeBy: sum
    		sourceColumn: invoice_item_number

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column signature_sk
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 228a8c98-2700-49ab-ab40-4cb42f44723b
    		summarizeBy: none
    		sourceColumn: signature_sk

    		annotation SummarizationSetBy = Automatic

    	column axis_sk
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 5a7b36bd-8ada-4ce2-96f7-4e58e4b6e0ad
    		summarizeBy: none
    		sourceColumn: axis_sk

    		annotation SummarizationSetBy = Automatic

    	column invoiced_units
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 89c063c0-f414-4bdb-812f-92d1f45b49e3
    		summarizeBy: sum
    		sourceColumn: invoiced_units

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column return_units
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 1022eabd-fd08-461b-bc26-d6a3920bfe79
    		summarizeBy: sum
    		sourceColumn: return_units

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column gross_sales
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 5e8482a3-0038-4e34-97ec-cae99bf5c64b
    		summarizeBy: sum
    		sourceColumn: gross_sales

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column gross_sales_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: c334ea4d-252c-4bbf-8dd1-b2f5c462d91e
    		summarizeBy: sum
    		sourceColumn: gross_sales_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column invoiced_sales
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 8273522e-cbbe-41c9-8ad2-1dfe7f129f3a
    		summarizeBy: sum
    		sourceColumn: invoiced_sales

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column invoiced_sales_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 1074ebd7-4046-4392-8fe0-783f25d7655d
    		summarizeBy: sum
    		sourceColumn: invoiced_sales_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column conso_net_sales
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: bce98926-38f0-410a-8af5-8b9846cb08cf
    		summarizeBy: sum
    		sourceColumn: conso_net_sales

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column conso_net_sales_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: a7811e1e-5146-4e5a-b488-c154b2eb0f95
    		summarizeBy: sum
    		sourceColumn: conso_net_sales_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column total_minorations
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: f2936996-fd6a-4631-b980-316c93dde56d
    		summarizeBy: sum
    		sourceColumn: total_minorations

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column total_minorations_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 85603f31-298d-400a-93c1-1e29c6f1d95f
    		summarizeBy: sum
    		sourceColumn: total_minorations_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column total_customers_allowances
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 89655f48-31c2-4c63-bc00-b66f493cdeb1
    		summarizeBy: sum
    		sourceColumn: total_customers_allowances

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column total_customers_allowances_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 68695be2-5a47-4084-adcd-cdb0c060765f
    		summarizeBy: sum
    		sourceColumn: total_customers_allowances_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column total_structural_discounts
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 701674d1-eab2-45f5-954c-6c8281ea4906
    		summarizeBy: sum
    		sourceColumn: total_structural_discounts

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column total_structural_discounts_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 6675d8e7-ce3f-4a55-a959-b59dbef6d2be
    		summarizeBy: sum
    		sourceColumn: total_structural_discounts_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column clearances
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 5dc04b42-03b2-4942-9622-1698bb3e07f4
    		summarizeBy: sum
    		sourceColumn: clearances

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column clearances_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 97790bfb-e126-4843-a61f-37988a8750e9
    		summarizeBy: sum
    		sourceColumn: clearances_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column total_returns
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: a33dfb58-0f6b-478a-997b-e87d6fbac7b8
    		summarizeBy: sum
    		sourceColumn: total_returns

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column total_returns_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: eab7658f-7dae-4af9-9bdb-6d4bde314f67
    		summarizeBy: sum
    		sourceColumn: total_returns_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column commercial_returns
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 1aecb012-88c3-467a-9e36-72375a14fbb3
    		summarizeBy: sum
    		sourceColumn: commercial_returns

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column commercial_returns_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: f8abd27b-ea9e-48d6-9f0f-0c4ceadabd30
    		summarizeBy: sum
    		sourceColumn: commercial_returns_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column returns_provisions
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 3ce05cad-1905-4551-8563-d0816af9de5f
    		summarizeBy: sum
    		sourceColumn: returns_provisions

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column returns_provisions_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: a1063be3-f083-4735-b19d-c3d776caff57
    		summarizeBy: sum
    		sourceColumn: returns_provisions_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column system_id
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: c5141400-ab23-440b-a9ef-500b41bec152
    		summarizeBy: none
    		sourceColumn: system_id

    		annotation SummarizationSetBy = Automatic

    	column source_system
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: c5cad28a-e199-4068-9f61-550957fc424b
    		summarizeBy: none
    		sourceColumn: source_system

    		annotation SummarizationSetBy = Automatic

    	column hub_sk
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: e94ff9f2-eea1-4caa-b3d3-29ddd5130b03
    		summarizeBy: none
    		sourceColumn: hub_sk

    		annotation SummarizationSetBy = Automatic

    	column source_flag
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: eadf4b50-0781-4d9b-8361-106d1273c163
    		summarizeBy: none
    		sourceColumn: source_flag

    		annotation SummarizationSetBy = Automatic

    	column sales_order_item_number
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: ebc13ded-0bf1-4654-8ebd-6d87aa40d87e
    		summarizeBy: none
    		sourceColumn: sales_order_item_number

    		annotation SummarizationSetBy = Automatic

    	column sales_order_document_type
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 94564de0-d720-4771-90f0-d541240607fe
    		summarizeBy: none
    		sourceColumn: sales_order_document_type

    		annotation SummarizationSetBy = Automatic

    	column sales_order_document_type_desc
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 5642ef79-518e-485b-b8ac-e7c4133cde9b
    		summarizeBy: none
    		sourceColumn: sales_order_document_type_desc

    		annotation SummarizationSetBy = Automatic

    	column product_sk
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: f483cd73-c9a1-4f1c-85b2-789bfa3d0055
    		summarizeBy: sum
    		sourceColumn: product_sk

    		annotation SummarizationSetBy = Automatic

    	column sales_product_sk
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: afc7cc2c-f874-4a91-b1ab-b1fa71bfb43b
    		summarizeBy: sum
    		sourceColumn: sales_product_sk

    		annotation SummarizationSetBy = Automatic

    	column sales_employee
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 53310dd6-874c-4493-9ec3-56d7c77ca498
    		summarizeBy: none
    		sourceColumn: sales_employee

    		annotation SummarizationSetBy = Automatic

    	column sales_group
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 59611a5b-718b-458b-8a5c-53129658b41b
    		summarizeBy: none
    		sourceColumn: sales_group

    		annotation SummarizationSetBy = Automatic

    	column sales_office
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: b71f99aa-8ff3-489b-a8d2-7ababf7a65af
    		summarizeBy: none
    		sourceColumn: sales_office

    		annotation SummarizationSetBy = Automatic

    	column rejection_reason
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 543f6b35-62fe-4ca2-a1de-f1e54adbc761
    		summarizeBy: none
    		sourceColumn: rejection_reason

    		annotation SummarizationSetBy = Automatic

    	column delivery_block
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 7e326fb0-baa9-48df-8236-c93d4c942861
    		summarizeBy: none
    		sourceColumn: delivery_block

    		annotation SummarizationSetBy = Automatic

    	column billing_block
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 0e7c27a2-924a-4371-a263-48a2b5887404
    		summarizeBy: none
    		sourceColumn: billing_block

    		annotation SummarizationSetBy = Automatic

    	column higher_level_bom
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: e9ca9f84-07ec-47fb-b7eb-2d8010f2cbec
    		summarizeBy: none
    		sourceColumn: higher_level_bom

    		annotation SummarizationSetBy = Automatic

    	column sales_customer_id
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 41473e93-3ade-43f4-8071-cf0cdb29edf2
    		summarizeBy: none
    		sourceColumn: sales_customer_id

    		annotation SummarizationSetBy = Automatic

    	column sales_customer_sk
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 651e1b37-9857-4799-bbd9-1bd8b3b5580d
    		summarizeBy: sum
    		sourceColumn: sales_customer_sk

    		annotation SummarizationSetBy = Automatic

    	column customer_ship_to
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 09fc36f6-e095-4577-b747-c05581abb45a
    		summarizeBy: none
    		sourceColumn: customer_ship_to

    		annotation SummarizationSetBy = Automatic

    	column sales_customer_ship_to_id
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 9e869d1e-1e16-4cfc-bb5c-e97164a1ba8b
    		summarizeBy: none
    		sourceColumn: sales_customer_ship_to_id

    		annotation SummarizationSetBy = Automatic

    	column sales_customer_ship_to_sk
    		dataType: int64
    		formatString: 0
    		sourceProviderType: bigint
    		lineageTag: 017b990c-5050-445f-b150-32385769e07a
    		summarizeBy: sum
    		sourceColumn: sales_customer_ship_to_sk

    		annotation SummarizationSetBy = Automatic

    	column has_goods_issue
    		dataType: boolean
    		formatString: """TRUE"";""TRUE"";""FALSE"""
    		sourceProviderType: bit
    		lineageTag: a89f045a-1e88-47a4-b1e3-e5e98dd79596
    		summarizeBy: none
    		sourceColumn: has_goods_issue

    		annotation SummarizationSetBy = Automatic

    	column open_order_sold_units
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: f9e3b7eb-1aba-4612-85e1-c2cd9b3de731
    		summarizeBy: sum
    		sourceColumn: open_order_sold_units

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column open_order_net_sales
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 0a70d28d-3da2-4fbe-a773-eb3f0b2ac0cb
    		summarizeBy: sum
    		sourceColumn: open_order_net_sales

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column open_order_net_sales_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: cd39fa3c-9a23-406c-9bf0-52a13ae4f814
    		summarizeBy: sum
    		sourceColumn: open_order_net_sales_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column open_order_plv_units
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 1b9158b6-aadc-4337-86c5-0cf9a6ee3b57
    		summarizeBy: sum
    		sourceColumn: open_order_plv_units

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column dni_sold_units
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 1cf35fd8-1902-47f0-ac63-7e9e53320a91
    		summarizeBy: sum
    		sourceColumn: dni_sold_units

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column dni_net_sales
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: ada80121-fee6-448e-8052-10dbe4420e67
    		summarizeBy: sum
    		sourceColumn: dni_net_sales

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column dni_net_sales_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 51ee8eb1-bb32-4ee8-a2a4-767a80020a04
    		summarizeBy: sum
    		sourceColumn: dni_net_sales_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column dni_plv_units
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 1fff933e-8f44-4f83-a784-ac208a0bd81f
    		summarizeBy: sum
    		sourceColumn: dni_plv_units

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column hub_desc
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 233438b9-0cc7-40ff-9e82-6b7579e6c1cf
    		summarizeBy: none
    		sourceColumn: hub_desc

    		annotation SummarizationSetBy = Automatic

    	column zone_desc
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: a0883c97-5c29-4435-b3d7-44c130e380c5
    		summarizeBy: none
    		sourceColumn: zone_desc

    		annotation SummarizationSetBy = Automatic

    	column signature_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 774e5f2a-15e2-4b0b-8f4f-fdf08b60fa3c
    		summarizeBy: none
    		sourceColumn: signature_code

    		annotation SummarizationSetBy = Automatic

    	column brand_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 77b6c9d3-f92c-408a-be54-7c115837a5a8
    		summarizeBy: none
    		sourceColumn: brand_code

    		annotation SummarizationSetBy = Automatic

    	column sub_brand_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 3ea500d1-1019-465c-bcff-019272a91e8d
    		summarizeBy: none
    		sourceColumn: sub_brand_code

    		annotation SummarizationSetBy = Automatic

    	column axis_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 22414657-cb89-4f93-9145-7bbb0d8cced2
    		summarizeBy: none
    		sourceColumn: axis_code

    		annotation SummarizationSetBy = Automatic

    	column customer_level_0_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 1040a884-09e4-4fba-a45a-ba36d76e9244
    		summarizeBy: none
    		sourceColumn: customer_level_0_code

    		annotation SummarizationSetBy = Automatic

    	column customer_level_3_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 612211a7-6c67-41aa-8517-2e9921d41a52
    		summarizeBy: none
    		sourceColumn: customer_level_3_code

    		annotation SummarizationSetBy = Automatic

    	column customer_level_4_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: c50f2462-b8ff-478c-978e-2d3f04823c3f
    		summarizeBy: none
    		sourceColumn: customer_level_4_code

    		annotation SummarizationSetBy = Automatic

    	column customer_level_5_code
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 21e82d91-da8b-4728-a149-f85541184b45
    		summarizeBy: none
    		sourceColumn: customer_level_5_code

    		annotation SummarizationSetBy = Automatic

    	column invoiced_sales_target
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 1f1532fb-d69e-439c-9f11-bd1f84644a24
    		summarizeBy: sum
    		sourceColumn: invoiced_sales_target

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column conso_net_sales_target
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 02fa04ec-e229-4da6-8a06-55b058891959
    		summarizeBy: sum
    		sourceColumn: conso_net_sales_target

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column invoiced_sales_target_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 6620fad4-7761-4b2a-8ccc-479302ac07b6
    		summarizeBy: sum
    		sourceColumn: invoiced_sales_target_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column conso_net_sales_target_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: ab061ec3-ec26-42f9-8398-a409d0282920
    		summarizeBy: sum
    		sourceColumn: conso_net_sales_target_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column invoiced_units_target
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 2a66ff98-e232-4e45-8585-24a3181c1697
    		summarizeBy: sum
    		sourceColumn: invoiced_units_target

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column total_portfolio_units
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: fab43875-d714-4cf7-b036-ab6cdb0f1067
    		summarizeBy: sum
    		sourceColumn: total_portfolio_units

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column unblocked_open_order_sold_units
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 72c32866-fd57-4034-86ad-e27bde33d225
    		summarizeBy: sum
    		sourceColumn: unblocked_open_order_sold_units

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column blocked_open_order_sold_units
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: abfcbfb5-f696-4389-905f-6753b11a51c6
    		summarizeBy: sum
    		sourceColumn: blocked_open_order_sold_units

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column unblocked_open_order_net_sales
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 2b37948e-37d2-456d-b66b-0dd93e71ec00
    		summarizeBy: sum
    		sourceColumn: unblocked_open_order_net_sales

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column unblocked_open_order_net_sales_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: af374a1c-c5bb-42d9-b13a-893965fe62ba
    		summarizeBy: sum
    		sourceColumn: unblocked_open_order_net_sales_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column blocked_open_order_net_sales
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: 26cb6c20-1ec0-4a8e-afbe-feb61e89d5b6
    		summarizeBy: sum
    		sourceColumn: blocked_open_order_net_sales

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column blocked_open_order_net_sales_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: b0a4aa6f-3687-4b6d-aad1-93a2787d7850
    		summarizeBy: sum
    		sourceColumn: blocked_open_order_net_sales_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column total_invoiced_sales_portfolio_in_eur
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: f31c4b16-eb8a-4fcf-a1cd-0e9242962344
    		summarizeBy: sum
    		sourceColumn: total_invoiced_sales_portfolio_in_eur

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	column total_invoiced_sales_portfolio
    		dataType: double
    		sourceProviderType: decimal(38, 9)
    		lineageTag: c147e5b4-a64c-48e7-a1d6-5f534c41e412
    		summarizeBy: sum
    		sourceColumn: total_invoiced_sales_portfolio

    		annotation SummarizationSetBy = Automatic

    		annotation PBI_FormatHint = {"isGeneralNumber":true}

    	partition fact_combined = m
    		mode: directQuery
    		source =
    				let
    				    Source = GoogleBigQueryAad.Database(GCP_Project, [Implementation=null, UseStorageApi=null, ConnectionTimeout=null, CommandTimeout=null, BYOID_AudienceUri=null, ProjectId=null]),
    				    GCP_Project1 = Source{[Name=GCP_Project]}[Data],
    				    GCP_DataSet = GCP_Project1{[Name=GCP_DataSet,Kind="Schema"]}[Data],
    				    DataSource = GCP_DataSet{[Name=PRM_fact_sellin,Kind="View"]}[Data]
    				in
    				    DataSource

    	annotation PBI_NavigationStepName = Navigation

    	annotation PBI_ResultType = Table

- path: definition/tables/KPI.tmdl
  payload: |+
    table KPI
    	lineageTag: 4797968f-7a75-44f2-b73f-f0b101968f38

    	column KPI
    		lineageTag: 3198bf99-0496-4db0-ba3e-814b782a9c9c
    		summarizeBy: none
    		sourceColumn: [Value1]
    		sortByColumn: 'KPI Order'

    		relatedColumnDetails
    			groupByColumn: 'KPI Fields'

    		annotation SummarizationSetBy = Automatic

    	column 'KPI Fields'
    		isHidden
    		lineageTag: 6cbb1cd6-4d97-4587-8986-cab2b6c3a0f3
    		summarizeBy: none
    		sourceColumn: [Value2]
    		sortByColumn: 'KPI Order'

    		extendedProperty ParameterMetadata =
    				{
    				  "version": 3,
    				  "kind": 2
    				}

    		annotation SummarizationSetBy = Automatic

    	column 'KPI Order'
    		isHidden
    		formatString: 0
    		lineageTag: 48d37873-3591-4fc3-be71-b71135bea027
    		summarizeBy: sum
    		sourceColumn: [Value3]

    		annotation SummarizationSetBy = Automatic

    	partition KPI = calculated
    		mode: import
    		source =
    				{
    				    ("Invoiced sales", NAMEOF('Measures_'[Invoiced sales N]), 0),
    				    ("Invoiced sales Y-1", NAMEOF('Measures_'[Y-1 INVOICED SALES]), 1),
    				    ("YTD INVOICED SALES", NAMEOF('Measures_'[YTD INVOICED SALES]), 2),
    				    ("Invoiced sales YOY %", NAMEOF('Measures_'[YOY % INVOICED SALES]), 3),
    				    ("Invoiced sales in EUR", NAMEOF('Measures_'[Invoiced sales in EUR N]), 4),
    				    ("Y-1 INVOICED SALES IN EUR", NAMEOF('Measures_'[Y-1 INVOICED SALES IN EUR]), 5),
    				    ("YTD INVOICED SALES IN EUR", NAMEOF('Measures_'[YTD INVOICED SALES IN EUR]), 6),
    				    ("YOY % INVOICED SALES IN EUR", NAMEOF('Measures_'[YOY % INVOICED SALES IN EUR]), 7),
    				    ("Conso net sales", NAMEOF('Measures_'[Conso net sales N]), 8),
    				    ("Conso net sales Y-1", NAMEOF('Measures_'[Y-1 CONSO NET SALES]), 9),
    				    ("YTD CONSO NET SALES", NAMEOF('Measures_'[YTD CONSO NET SALES]), 10),
    				    ("Conso net sales YOY %", NAMEOF('Measures_'[YOY % CONSO NET SALES]), 11),
    				    ("Conso net sales in EUR", NAMEOF('Measures_'[Conso net sales in EUR N]), 12),
    				    ("Y-1 CONSO NET SALES IN EUR", NAMEOF('Measures_'[Y-1 CONSO NET SALES IN EUR]), 13),
    				    ("YTD CONSO NET SALES IN EUR", NAMEOF('Measures_'[YTD CONSO NET SALES IN EUR]), 14),
    				    ("YOY % CONSO NET SALES IN EUR", NAMEOF('Measures_'[YOY % CONSO NET SALES IN EUR]), 15),
    				    ("Total Sales", NAMEOF('Measures_'[Total Sales N]), 16),
    				    ("Total Sales Y-1 ", NAMEOF('Measures_'[Y-1 TOTAL SALES]), 17),
    				    ("YTD TOTAL SALES", NAMEOF('Measures_'[YTD TOTAL SALES]), 18),
    				    ("Total Sales YOY % ", NAMEOF('Measures_'[YOY % TOTAL SALES]), 19),
    				    ("Total Sales EUR", NAMEOF('Measures_'[Total Sales in EUR N] ), 20),
    				    ("Y-1 TOTAL SALES in EUR", NAMEOF('Measures_'[Y-1 TOTAL SALES in EUR]), 21),
    				    ("YTD TOTAL SALES IN EUR", NAMEOF('Measures_'[YTD TOTAL SALES IN EUR]), 22),
    				    ("YOY % TOTAL SALES IN EUR", NAMEOF('Measures_'[YOY % TOTAL SALES IN EUR]), 23),
    				    ("Total minorations", NAMEOF('Measures_'[Total minorations N]), 24),
    				    ("MTD TOTAL MINORATIONS", NAMEOF('Measures_'[MTD TOTAL MINORATIONS]), 25),
    				    ("Y-1 TOTAL MINORATIONS", NAMEOF('Measures_'[Y-1 TOTAL MINORATIONS]), 26),
    				    ("YTD TOTAL MINORATIONS", NAMEOF('Measures_'[YTD TOTAL MINORATIONS]), 27),
    				    ("YOY % TOTAL MINORATIONS", NAMEOF('Measures_'[YOY % TOTAL MINORATIONS]), 28),
    				    ("Total minorations in EUR", NAMEOF('Measures_'[Total minorationsin EUR N]), 29),
    				    ("MTD TOTAL MINORATIONS IN EUR", NAMEOF('Measures_'[MTD TOTAL MINORATIONS IN EUR]), 30),
    				    ("Y-1 TOTAL MINORATIONS IN EUR", NAMEOF('Measures_'[Y-1 TOTAL MINORATIONS IN EUR]), 31),
    				    ("YTD TOTAL MINORATIONS IN EUR", NAMEOF('Measures_'[YTD TOTAL MINORATIONS IN EUR]), 32),
    				    ("YOY % TOTAL MINORATIONS in EUR", NAMEOF('Measures_'[YOY % TOTAL MINORATIONS in EUR]), 33),
    				    ("Total customers allowances", NAMEOF('Measures_'[Total customers allowances N]), 34),
    				    ("MTD TOTAL CUSTOMER ALLOWANCE IN EUR", NAMEOF('Measures_'[MTD TOTAL CUSTOMER ALLOWANCE IN EUR]), 35),
    				    ("Y-1 TOTAL CUSTOMERS ALLOWANCES", NAMEOF('Measures_'[Y-1 TOTAL CUSTOMERS ALLOWANCES]), 36),
    				    ("YTD TOTAL CUSTOMER ALLOWANCES", NAMEOF('Measures_'[YTD TOTAL CUSTOMER ALLOWANCES]), 37),
    				    ("YOY % TOTAL CUSTOMER ALLOWANCES", NAMEOF('Measures_'[YOY % TOTAL CUSTOMER ALLOWANCES]), 38),
    				    ("Total customers allowances in EUR", NAMEOF('Measures_'[Total customers allowances in EUR N]), 39),
    				    ("MTD TOTAL CUSTOMERS ALLOWANCES", NAMEOF('Measures_'[MTD TOTAL CUSTOMERS ALLOWANCES]), 40),
    				    ("Y-1 TOTAL CUSTOMERS ALLOWANCES IN EUR", NAMEOF('Measures_'[Y-1 TOTAL CUSTOMERS ALLOWANCES IN EUR]), 41),
    				    ("YTD TOTAL CUSTOMER ALLOWANCES IN EUR", NAMEOF('Measures_'[YTD TOTAL CUSTOMER ALLOWANCES IN EUR]), 42),
    				    ("YOY % TOTAL CUSTOMER ALLOWANCES IN EUR", NAMEOF('Measures_'[YOY % TOTAL CUSTOMER ALLOWANCES IN EUR]), 43),
    				    ("Total structural discounts", NAMEOF('Measures_'[Total structural discounts N]), 44),
    				    ("MTD TOTAL STRUCTURAL DISCOUNTS", NAMEOF('Measures_'[MTD TOTAL STRUCTURAL DISCOUNTS]), 45),
    				    ("Y-1 TOTAL STRUCTURAL DISCOUNTS", NAMEOF('Measures_'[Y-1 TOTAL STRUCTURAL DISCOUNTS]), 46),
    				    ("YTD TOTAL STRUCTURAL DISCOUNTS", NAMEOF('Measures_'[YTD TOTAL STRUCTURAL DISCOUNTS]), 47),
    				    ("YOY % TOTAL STRUCTURAL DISCOUNTS", NAMEOF('Measures_'[YOY % TOTAL STRUCTURAL DISCOUNTS]), 48),
    				    ("MTD TOTAL STRUCTURAL DISCOUNTS IN EUR", NAMEOF('Measures_'[MTD TOTAL STRUCTURAL DISCOUNTS IN EUR]), 49),
    				    ("Y-1 TOTAL STRUCTURAL DISCOUNTS IN EUR", NAMEOF('Measures_'[Y-1 TOTAL STRUCTURAL DISCOUNTS IN EUR]), 50),
    				    ("YTD TOTAL STRUCTURAL DISCOUNTS IN EUR", NAMEOF('Measures_'[YTD TOTAL STRUCTURAL DISCOUNTS IN EUR]), 51),
    				    ("YOY % TOTAL STRUCTURAL DISCOUNTS IN EUR", NAMEOF('Measures_'[YOY % TOTAL STRUCTURAL DISCOUNTS IN EUR]), 52),
    				    ("Clearances", NAMEOF('Measures_'[Clearances N]), 53),
    				    ("MTD CLEARANCES IN EUR", NAMEOF('Measures_'[MTD CLEARANCES IN EUR]), 54),
    				    ("Y-1 CLEAREANCES", NAMEOF('Measures_'[Y-1 CLEAREANCES]), 55),
    				    ("YTD CLEAREANCES", NAMEOF('Measures_'[YTD CLEAREANCES]), 56),
    				    ("YOY % CLEAREANCES", NAMEOF('Measures_'[YOY % CLEAREANCES]), 57),
    				    ("Clearances in EUR", NAMEOF('Measures_'[Clearances in EUR N]), 58),
    				    ("MTD CLEAREANCES", NAMEOF('Measures_'[MTD CLEAREANCES]), 59),
    				    ("Y-1 CLEAREANCES IN EUR", NAMEOF('Measures_'[Y-1 CLEAREANCES IN EUR]), 60),
    				    ("YTD CLEAREANCES IN EUR", NAMEOF('Measures_'[YTD CLEAREANCES IN EUR]), 61),
    				    ("YOY % CLEAREANCES IN EUR", NAMEOF('Measures_'[YOY % CLEAREANCES IN EUR]), 62),
    				    ("Total returns", NAMEOF('Measures_'[Total returns N]), 63),
    				    ("MTD TOTAL RETURENS", NAMEOF('Measures_'[MTD TOTAL RETURENS]), 64),
    				    ("Y-1 TOTAL RETURENS", NAMEOF('Measures_'[Y-1 TOTAL RETURENS]), 65),
    				    ("YTD TOTAL RETURENS", NAMEOF('Measures_'[YTD TOTAL RETURENS]), 66),
    				    ("YOY % TOTAL RETURENS", NAMEOF('Measures_'[YOY % TOTAL RETURENS]), 67),
    				    ("total returns in eur", NAMEOF('Measures_'[Total returns in EUR N]), 68),
    				    ("MTD TOTAL RETURENS IN EUR", NAMEOF('Measures_'[MTD TOTAL RETURENS IN EUR]), 69),
    				    ("Y-1 TOTAL RETURNS IN EUR", NAMEOF('Measures_'[Y-1 TOTAL RETURNS IN EUR]), 70),
    				    ("YTD TOTAL RETURENS IN EUR", NAMEOF('Measures_'[YTD TOTAL RETURENS IN EUR]), 71),
    				    ("YOY % TOTAL RETURENS IN EUR", NAMEOF('Measures_'[YOY % TOTAL RETURENS IN EUR]), 72),
    				    ("Commercial returns", NAMEOF('Measures_'[Commercial returns N]), 73),
    				    ("MTD COMMERCIAL RETURNS", NAMEOF('Measures_'[MTD COMMERCIAL RETURNS]), 74),
    				    ("Y-1 COMMERCIAL RETURNS", NAMEOF('Measures_'[Y-1 COMMERCIAL RETURNS]), 75),
    				    ("YTD COMMERCIAL RETURNS", NAMEOF('Measures_'[YTD COMMERCIAL RETURNS]), 76),
    				    ("YOY % COMMERCIAL RETURNS", NAMEOF('Measures_'[YOY % COMMERCIAL RETURNS]), 77),
    				    ("Commercial returns in EUR", NAMEOF('Measures_'[Commercial returns in EUR N]), 78),
    				    ("MTD COMMERCIAL RETURNS IN EUR", NAMEOF('Measures_'[MTD COMMERCIAL RETURNS IN EUR]), 79),
    				    ("Y-1 COMMERCIAL RETURNS IN EUR", NAMEOF('Measures_'[Y-1 COMMERCIAL RETURNS IN EUR]), 80),
    				    ("YTD COMMERCIAL RETURNS IN EUR", NAMEOF('Measures_'[YTD COMMERCIAL RETURNS IN EUR]), 81),
    				    ("YOY % COMMERCIAL RETURNS IN EUR", NAMEOF('Measures_'[YOY % COMMERCIAL RETURNS IN EUR]), 82),
    				    ("Returns provisions", NAMEOF('Measures_'[Returns provisions N]), 83),
    				    ("MTD RETURNS PROVISION", NAMEOF('Measures_'[MTD RETURNS PROVISION]), 84),
    				    ("Y-1 RETURNS PROVISION", NAMEOF('Measures_'[Y-1 RETURNS PROVISION]), 85),
    				    ("YTD RETURNS PROVISION", NAMEOF('Measures_'[YTD RETURNS PROVISION]), 86),
    				    ("YOY % RETURNS PROVISION", NAMEOF('Measures_'[YOY % RETURNS PROVISION]), 87),
    				    ("Returns provisions in EUR", NAMEOF('Measures_'[Returns provisions in EUR N]), 88),
    				    ("MTD RETURNS PROVISIONS IN EUR", NAMEOF('Measures_'[MTD RETURNS PROVISIONS IN EUR]), 89),
    				    ("Y-1 RETURNS PROVISION IN EUR", NAMEOF('Measures_'[Y-1 RETURNS PROVISION IN EUR]), 90),
    				    ("YTD RETURNS PROVISION IN EUR", NAMEOF('Measures_'[YTD RETURNS PROVISION IN EUR]), 91),
    				    ("YOY % RETURNS PROVISION IN EUR", NAMEOF('Measures_'[YOY % RETURNS PROVISION IN EUR]), 92),
    				    ("MTD % CNS TARGET REACHED", NAMEOF('Measures_'[MTD % CNS TARGET REACHED]), 93),
    				    ("Y-1 % CNS TARGET REACHED", NAMEOF('Measures_'[Y-1 % CNS TARGET REACHED]), 94),
    				    ("YTD % CNS TARGET REACHED", NAMEOF('Measures_'[YTD % CNS TARGET REACHED]), 95),
    				    ("YOY % CNS TARGET REACHED", NAMEOF('Measures_'[YOY % CNS TARGET REACHED]), 96),
    				    ("MTD % IS TARGET REACHED", NAMEOF('Measures_'[MTD % IS TARGET REACHED]), 97),
    				    ("Y-1 % IS TARGET REACHED", NAMEOF('Measures_'[Y-1 % IS TARGET REACHED]), 98),
    				    ("YTD % IS TARGET REACHED", NAMEOF('Measures_'[YTD % IS TARGET REACHED]), 99),
    				    ("YOY % IS TARGET REACHED", NAMEOF('Measures_'[YOY % IS TARGET REACHED]), 100),
    				    ("MTD BLOCKED OPEN ORDERS IN UNITS", NAMEOF('Measures_'[MTD BLOCKED OPEN ORDERS IN UNITS]), 101),
    				    ("MTD BLOCKED OPEN ORDERS VALUE", NAMEOF('Measures_'[MTD BLOCKED OPEN ORDERS VALUE]), 102),
    				    ("MTD BLOCKED OPEN ORDERS VALUE IN EUR", NAMEOF('Measures_'[MTD BLOCKED OPEN ORDERS VALUE IN EUR]), 103),
    				    ("MTD UNBLOCKED OPEN ORDERS IN UNITS", NAMEOF('Measures_'[MTD UNBLOCKED OPEN ORDERS IN UNITS]), 104),
    				    ("MTD UNBLOCKED OPEN ORDERS VALUE", NAMEOF('Measures_'[MTD UNBLOCKED OPEN ORDERS VALUE]), 105),
    				    ("MTD UNBLOCKED OPEN ORDERS VALUE IN EURO", NAMEOF('Measures_'[MTD UNBLOCKED OPEN ORDERS VALUE IN EURO]), 106),
    				    ("MTD TOTAL SALES", NAMEOF('Measures_'[MTD TOTAL SALES]), 107),
    				    ("MTD TOTAL SALES in EUR", NAMEOF('Measures_'[MTD TOTAL SALES in EUR]), 108),
    				    ("Y-1 BLOCKED OPEN ORDERS IN UNITS", NAMEOF('Measures_'[Y-1 BLOCKED OPEN ORDERS IN UNITS]), 109),
    				    ("Y-1 BLOCKED OPEN ORDERS VALUE", NAMEOF('Measures_'[Y-1 BLOCKED OPEN ORDERS VALUE]), 110),
    				    ("Y-1 BLOCKED OPEN ORDERS VALUE IN EUR", NAMEOF('Measures_'[Y-1 BLOCKED OPEN ORDERS VALUE IN EUR]), 111),
    				    ("Y-1 UNBLOCKED OPEN ORDERS IN UNITS", NAMEOF('Measures_'[Y-1 UNBLOCKED OPEN ORDERS IN UNITS]), 112),
    				    ("Y-1 UNBLOCKED OPEN ORDERS VALUE", NAMEOF('Measures_'[Y-1 UNBLOCKED OPEN ORDERS VALUE]), 113),
    				    ("Y-1 UNBLOCKED OPEN ORDERS VALUE IN EURO", NAMEOF('Measures_'[Y-1 UNBLOCKED OPEN ORDERS VALUE IN EURO]), 114),
    				    ("YTD BLOCKED OPEN ORDERS IN UNITS", NAMEOF('Measures_'[YTD BLOCKED OPEN ORDERS IN UNITS]), 115),
    				    ("YTD BLOCKED OPEN ORDERS VALUE", NAMEOF('Measures_'[YTD BLOCKED OPEN ORDERS VALUE]), 116),
    				    ("YTD BLOCKED OPEN ORDERS VALUE IN EUR", NAMEOF('Measures_'[YTD BLOCKED OPEN ORDERS VALUE IN EUR]), 117),
    				    ("YTD UNBLOCKED OPEN ORDERS IN UNITS", NAMEOF('Measures_'[YTD UNBLOCKED OPEN ORDERS IN UNITS]), 118),
    				    ("YTD UNBLOCKED OPEN ORDERS VALUE", NAMEOF('Measures_'[YTD UNBLOCKED OPEN ORDERS VALUE]), 119),
    				    ("YTD UNBLOCKED OPEN ORDERS VALUE IN EURO", NAMEOF('Measures_'[YTD UNBLOCKED OPEN ORDERS VALUE IN EURO]), 120),
    				    ("YOY % BLOCKED OPEN ORDERS IN UNITS", NAMEOF('Measures_'[YOY % BLOCKED OPEN ORDERS IN UNITS]), 121),
    				    ("YOY % BLOCKED OPEN ORDERS VALUE", NAMEOF('Measures_'[YOY % BLOCKED OPEN ORDERS VALUE]), 122),
    				    ("YOY % BLOCKED OPEN ORDERS VALUE IN EUR", NAMEOF('Measures_'[YOY % BLOCKED OPEN ORDERS VALUE IN EUR]), 123),
    				    ("YOY % UNBLOCKED OPEN ORDERS IN UNITS", NAMEOF('Measures_'[YOY % UNBLOCKED OPEN ORDERS IN UNITS]), 124),
    				    ("YOY % UNBLOCKED OPEN ORDERS VALUE", NAMEOF('Measures_'[YOY % UNBLOCKED OPEN ORDERS VALUE]), 125),
    				    ("YOY % UNBLOCKED OPEN ORDERS VALUE IN EURO", NAMEOF('Measures_'[YOY % UNBLOCKED OPEN ORDERS VALUE IN EURO]), 126)
    				}

    	annotation PBI_Id = 57ee4bdbaa3f457da330df69f42abde3

- path: definition/tables/customGroup.tmdl
  payload: |+
    table customGroup
    	lineageTag: b095604f-4597-4bb6-bb67-77f8de920af1

    	column 'Subbrand code'
    		dataType: string
    		lineageTag: 020a623b-ed07-4004-a89c-dfd9ac104c1e
    		summarizeBy: none
    		sourceColumn: Subbrand code

    		annotation SummarizationSetBy = Automatic

    	column 'Custom subbrand group'
    		dataType: string
    		lineageTag: 8b4fece6-955d-4095-91ea-fb5293c6969b
    		summarizeBy: none
    		sourceColumn: Custom subbrand group

    		annotation SummarizationSetBy = Automatic

    	partition customGroup = m
    		mode: import
    		source =
    				let
    				    Source = Excel.Workbook(Web.Contents("https://loreal-my.sharepoint.com/personal/swathi_subramanian_loreal_com/Documents/Fichiers%20de%20conversation%20Microsoft%20Teams/customExternalFile1.xlsx"), null, true),
    				    customGroup_Sheet = Source{[Item="customGroup",Kind="Sheet"]}[Data],
    				    #"Changed Type" = Table.TransformColumnTypes(customGroup_Sheet,{{"Column1", type text}, {"Column2", type text}}),
    				    #"Promoted Headers" = Table.PromoteHeaders(#"Changed Type", [PromoteAllScalars=true]),
    				    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers",{{"subbrand_code", type text}, {"custom_subbrand_group", type text}}),
    				    #"Renamed Columns" = Table.RenameColumns(#"Changed Type1",{{"subbrand_code", "Subbrand code"}, {"custom_subbrand_group", "Custom subbrand group"}}),
    				    #"Uppercased Text" = Table.TransformColumns(#"Renamed Columns",{{"Subbrand code", Text.Upper, type text}}),
    				    #"Removed Duplicates" = Table.Distinct(#"Uppercased Text", {"Subbrand code"}),
    				    #"Filtered Rows" = Table.SelectRows(#"Removed Duplicates", each [Subbrand code] <> null and [Subbrand code] <> "")
    				in
    				    #"Filtered Rows"

    	annotation PBI_ResultType = Table

    	annotation PBI_NavigationStepName = Navigation

- path: definition/tables/TI_Table.tmdl
  payload: |+
    table TI_Table
    	lineageTag: 4f4e5ee8-dc9c-4685-8505-ef1eb5ed6793

    	column data_analysis
    		dataType: dateTime
    		formatString: Short Date
    		sourceProviderType: date
    		lineageTag: 01c586da-5c72-463b-b46f-afecac435a9e
    		summarizeBy: none
    		sourceColumn: data_analysis

    		variation Variation
    			isDefault
    			relationship: d414111a-9160-45b0-a5ee-a5c7475bd7e8
    			defaultHierarchy: LocalDateTable_f992abc6-6c6f-467b-915f-f7ab15fee947.'Date Hierarchy'

    		annotation SummarizationSetBy = Automatic

    		annotation UnderlyingDateTimeDataType = Date

    	column date_relation
    		dataType: dateTime
    		formatString: Long Date
    		sourceProviderType: date
    		lineageTag: 306fd98d-b6c4-4dc1-8b51-0243c1827e9d
    		summarizeBy: none
    		sourceColumn: date_relation

    		variation Variation
    			isDefault
    			relationship: fadb45dc-ed67-4300-a646-99f60b280560
    			defaultHierarchy: LocalDateTable_a10507c8-3a5a-4373-a663-4cfa3ae454b6.'Date Hierarchy'

    		annotation SummarizationSetBy = Automatic

    		annotation UnderlyingDateTimeDataType = Date

    	column Period
    		dataType: string
    		sourceProviderType: nvarchar(16384)
    		lineageTag: 854c3b81-26ba-4865-b7b1-8b75dbd30517
    		summarizeBy: none
    		sourceColumn: Period

    		annotation SummarizationSetBy = Automatic

    	partition TI_Table = m
    		mode: import
    		source =
    				let
    				    Source = GoogleBigQueryAad.Database(GCP_Project, [Implementation=null, UseStorageApi=null, ConnectionTimeout=null, CommandTimeout=null, BYOID_AudienceUri=null, ProjectId=null]),
    				    GCP_Project1 = Source{[Name=GCP_Project]}[Data],
    				    GCP_DataSet = GCP_Project1{[Name=GCP_DataSet,Kind="Schema"]}[Data],
    				    dim_signature_View = GCP_DataSet{[Name="time_intelligence",Kind="Table"]}[Data],
    				    #"Renamed Columns" = Table.RenameColumns(dim_signature_View,{{"period", "Period"}})
    				in
    				    #"Renamed Columns"

    	annotation PBI_NavigationStepName = Navigation

    	annotation PBI_ResultType = Table

- path: definition/tables/LocalDateTable_f992abc6-6c6f-467b-915f-f7ab15fee947.tmdl
  payload: |+
    table LocalDateTable_f992abc6-6c6f-467b-915f-f7ab15fee947
    	isHidden
    	showAsVariationsOnly
    	lineageTag: 4def49e6-2006-47ac-bbf0-84e1d1ef6cfe

    	column Date
    		dataType: dateTime
    		isHidden
    		lineageTag: 1607b591-c1be-4ca5-9a0d-bdae826540c9
    		dataCategory: PaddedDateTableDates
    		summarizeBy: none
    		isNameInferred
    		sourceColumn: [Date]

    		annotation SummarizationSetBy = User

    	column Year = YEAR([Date])
    		dataType: int64
    		isHidden
    		lineageTag: 0833b9c7-7f5b-4633-b2b2-a8604fcd1de0
    		dataCategory: Years
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Year

    	column MonthNo = MONTH([Date])
    		dataType: int64
    		isHidden
    		lineageTag: d09b93c4-c767-4514-9fef-279e6dbabce1
    		dataCategory: MonthOfYear
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = MonthNumber

    	column Month = FORMAT([Date], "MMMM")
    		dataType: string
    		isHidden
    		lineageTag: 57cd173d-a4fd-40b2-a66f-d18ef2912a0d
    		dataCategory: Months
    		summarizeBy: none
    		sortByColumn: MonthNo

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Month

    	column QuarterNo = INT(([MonthNo] + 2) / 3)
    		dataType: int64
    		isHidden
    		lineageTag: 5df4ddc6-addc-4e24-a9bf-9b4695d231ae
    		dataCategory: QuarterOfYear
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = QuarterNumber

    	column Quarter = "Qtr " & [QuarterNo]
    		dataType: string
    		isHidden
    		lineageTag: 64abd184-53d3-40fd-8cdf-6303276dc03f
    		dataCategory: Quarters
    		summarizeBy: none
    		sortByColumn: QuarterNo

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Quarter

    	column Day = DAY([Date])
    		dataType: int64
    		isHidden
    		lineageTag: fbcec585-381b-4a39-8333-478c0560fd48
    		dataCategory: DayOfMonth
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Day

    	hierarchy 'Date Hierarchy'
    		lineageTag: eeeb07ed-791d-41b2-872f-6c78fe9a2e95

    		level Year
    			lineageTag: efdb6340-5aa5-4dd7-a1f6-4d22734a2db8
    			column: Year

    		level Quarter
    			lineageTag: 929b5e83-81aa-4eca-803f-a31848a5f6c1
    			column: Quarter

    		level Month
    			lineageTag: f5069e5f-7e62-4338-9a77-6ae9ac100255
    			column: Month

    		level Day
    			lineageTag: 0161cf77-96c4-4697-8f41-376d45f57a87
    			column: Day

    		annotation TemplateId = DateHierarchy

    	partition LocalDateTable_f992abc6-6c6f-467b-915f-f7ab15fee947 = calculated
    		mode: import
    		source = Calendar(Date(Year(MIN('TI_Table'[data_analysis])), 1, 1), Date(Year(MAX('TI_Table'[data_analysis])), 12, 31))

    	annotation __PBI_LocalDateTable = true

- path: definition/tables/LocalDateTable_a10507c8-3a5a-4373-a663-4cfa3ae454b6.tmdl
  payload: |+
    table LocalDateTable_a10507c8-3a5a-4373-a663-4cfa3ae454b6
    	isHidden
    	showAsVariationsOnly
    	lineageTag: 81bb74d2-c47c-4f94-91ba-4b92814fbe43

    	column Date
    		dataType: dateTime
    		isHidden
    		lineageTag: b166306c-e1f1-41c1-9694-25022720b69b
    		dataCategory: PaddedDateTableDates
    		summarizeBy: none
    		isNameInferred
    		sourceColumn: [Date]

    		annotation SummarizationSetBy = User

    	column Year = YEAR([Date])
    		dataType: int64
    		isHidden
    		lineageTag: 3a659f3a-df3c-433d-8b0a-ea00c6e2b652
    		dataCategory: Years
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Year

    	column MonthNo = MONTH([Date])
    		dataType: int64
    		isHidden
    		lineageTag: 1445856e-7cb8-48d1-b412-ecf93b4972e9
    		dataCategory: MonthOfYear
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = MonthNumber

    	column Month = FORMAT([Date], "MMMM")
    		dataType: string
    		isHidden
    		lineageTag: 43f4e895-5eff-40f8-8954-c8fe86cdb72c
    		dataCategory: Months
    		summarizeBy: none
    		sortByColumn: MonthNo

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Month

    	column QuarterNo = INT(([MonthNo] + 2) / 3)
    		dataType: int64
    		isHidden
    		lineageTag: 7c6ad7fb-0529-440f-8097-5d7c56eb90a5
    		dataCategory: QuarterOfYear
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = QuarterNumber

    	column Quarter = "Qtr " & [QuarterNo]
    		dataType: string
    		isHidden
    		lineageTag: 51284695-f6a3-42f2-bc6b-2077ba6a844d
    		dataCategory: Quarters
    		summarizeBy: none
    		sortByColumn: QuarterNo

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Quarter

    	column Day = DAY([Date])
    		dataType: int64
    		isHidden
    		lineageTag: 6975eb8f-1939-4dd5-85ae-ad1a25e67216
    		dataCategory: DayOfMonth
    		summarizeBy: none

    		annotation SummarizationSetBy = User

    		annotation TemplateId = Day

    	hierarchy 'Date Hierarchy'
    		lineageTag: 6b08978d-9ebf-4f82-beca-8251b46cefbb

    		level Year
    			lineageTag: c74a06d5-77db-4d5c-b8b8-b3e668ccb239
    			column: Year

    		level Quarter
    			lineageTag: 097167fb-15e4-4dc4-b994-09bbc119fcad
    			column: Quarter

    		level Month
    			lineageTag: 3c6d6fd7-15b6-4603-b5e6-844a3ab21d7f
    			column: Month

    		level Day
    			lineageTag: 1ccc9b0b-635d-4429-a5a4-fad59b524f0c
    			column: Day

    		annotation TemplateId = DateHierarchy

    	partition LocalDateTable_a10507c8-3a5a-4373-a663-4cfa3ae454b6 = calculated
    		mode: import
    		source = Calendar(Date(Year(MIN('TI_Table'[date_relation])), 1, 1), Date(Year(MAX('TI_Table'[date_relation])), 12, 31))

    	annotation __PBI_LocalDateTable = true

- path: definition/tables/Selin.tmdl
  payload: |+
    table Selin
    	lineageTag: d2a6067d-4392-45fe-846e-1958b929f068

    	column Combined
    		dataType: string
    		lineageTag: f193ccb9-4fc0-4886-bec4-872fbf70e090
    		summarizeBy: none
    		sourceColumn: Combined

    		extendedProperty ParameterMetadata =
    				{
    				  "version": 2,
    				  "kind": 1,
    				  "selectAllValue": "__SelectAll__"
    				}

    		annotation SummarizationSetBy = Automatic

    	partition Selin = m
    		mode: import
    		source =
    				let
    				    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WSktMLokvKS3Kyy9LLYpPzs9NysxLTYkvTk0uLQLShoZJSrE6RCjLJ0aZsSkxqooMDZViYwE=", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [combined = _t]),
    				    #"Renamed Columns" = Table.RenameColumns(Source,{{"combined", "Combined"}})
    				in
    				    #"Renamed Columns"

    	annotation PBI_NavigationStepName = Navigation

    	annotation PBI_ResultType = Table

- path: definition/relationships.tmdl
  payload: |+
    relationship cf45b04a-7fb1-4e6e-a716-950afe3e6832
    	joinOnDateBehavior: datePartOnly
    	fromColumn: Date.Date
    	toColumn: LocalDateTable_bc1da608-328f-482f-89bd-aa0b143b50f1.Date

    relationship aeb10df0-15c7-3577-3fef-c9268585a042
    	fromColumn: fact_combined.axis_sk
    	toColumn: dim_axis.axis_sk

    relationship daf40d37-33f4-815c-0bb6-9f9b1ee4747c
    	relyOnReferentialIntegrity
    	fromColumn: fact_combined.sales_customer_tech_fk
    	toColumn: dim_sales_customer.sales_customer_tech_unique_id

    relationship 93cfd8e5-7d27-7a97-f60e-0b7f3d05b455
    	fromColumn: fact_combined.product_tech_fk
    	toColumn: dim_product.product_tech_unique_id

    relationship 2555dfe2-1b32-5fde-b713-40d9999e75cf
    	fromColumn: fact_combined.product_sales_area_tech_fk
    	toColumn: dim_sales_product.product_sales_area_tech_unique_id

    relationship 8537f27e-0408-6459-6ef7-9bebbf0a4cad
    	fromColumn: fact_combined.date
    	toColumn: Date.Date

    relationship 4572f075-191f-3ffd-e4c3-1f676e21f18a
    	fromColumn: dim_product.'Sub brand code'
    	toColumn: customGroup.'Subbrand code'

    relationship 0ba7113c-5515-f4a1-a6ba-b8d5ca449784
    	fromColumn: fact_combined.hub_sk
    	toColumn: dim_hub.hub_sk

    relationship 0d8504cf-ff9e-736b-6cc7-8e1dcb7c38d2
    	fromColumn: fact_combined.signature_sk
    	toColumn: dim_signature.signature_sk

    relationship bed1d10b-6bd9-fada-b639-8f57e12f9161
    	toCardinality: many
    	fromColumn: fact_combined.date
    	toColumn: TI_Table.date_relation

    relationship d414111a-9160-45b0-a5ee-a5c7475bd7e8
    	joinOnDateBehavior: datePartOnly
    	fromColumn: TI_Table.data_analysis
    	toColumn: LocalDateTable_f992abc6-6c6f-467b-915f-f7ab15fee947.Date

    relationship fadb45dc-ed67-4300-a646-99f60b280560
    	joinOnDateBehavior: datePartOnly
    	fromColumn: TI_Table.date_relation
    	toColumn: LocalDateTable_a10507c8-3a5a-4373-a663-4cfa3ae454b6.Date

- path: definition/cultures/en-US.tmdl
  payload: |+
    cultureInfo en-US

    	linguisticMetadata =
    			{
    			  "Version": "2.0.0",
    			  "Language": "en-US",
    			  "Entities": {
    			    "measures_.mtd__cns_target_reached": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "MTD % CNS TARGET REACHED"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.mtd_blocked_open_orders_in_units": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "MTD BLOCKED OPEN ORDERS IN UNITS"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.mtd_blocked_open_orders_value": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "MTD BLOCKED OPEN ORDERS VALUE"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.mtd_blocked_open_orders_value_in_eur": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "MTD BLOCKED OPEN ORDERS VALUE IN EUR"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.mtd_unblocked_open_orders_in_units": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "MTD UNBLOCKED OPEN ORDERS IN UNITS"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.mtd_unblocked_open_orders_value": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "MTD UNBLOCKED OPEN ORDERS VALUE"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.mtd_unblocked_open_orders_value_in_euro": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "MTD UNBLOCKED OPEN ORDERS VALUE IN EURO"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.mtd_total_sales": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "MTD TOTAL SALES"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.mtd_total_sales_in_eur": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "MTD TOTAL SALES in EUR"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.yoy__blocked_open_orders_in_units": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YOY % BLOCKED OPEN ORDERS IN UNITS"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.yoy__blocked_open_orders_value": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YOY % BLOCKED OPEN ORDERS VALUE"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.yoy__blocked_open_orders_value_in_eur": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YOY % BLOCKED OPEN ORDERS VALUE IN EUR"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.yoy__unblocked_open_orders_in_units": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YOY % UNBLOCKED OPEN ORDERS IN UNITS"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.yoy__unblocked_open_orders_value": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YOY % UNBLOCKED OPEN ORDERS VALUE"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.yoy__unblocked_open_orders_value_in_euro": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YOY % UNBLOCKED OPEN ORDERS VALUE IN EURO"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.y1_total_sales": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Y-1 TOTAL SALES"
    			        }
    			      },
    			      "State": "Generated",
    			      "Terms": [
    			        {
    			          "Total Sales Y-1": {
    			            "State": "Suggested",
    			            "Source": {
    			              "Type": "External",
    			              "Agent": "PowerBI.VisualColumnRename"
    			            },
    			            "Weight": 0.9
    			          }
    			        }
    			      ]
    			    },
    			    "measures_.y1_blocked_open_orders_in_units": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Y-1 BLOCKED OPEN ORDERS IN UNITS"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.y1_blocked_open_orders_value": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Y-1 BLOCKED OPEN ORDERS VALUE"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.y1_blocked_open_orders_value_in_eur": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Y-1 BLOCKED OPEN ORDERS VALUE IN EUR"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.y1_unblocked_open_orders_in_units": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Y-1 UNBLOCKED OPEN ORDERS IN UNITS"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.y1_unblocked_open_orders_value_in_euro": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Y-1 UNBLOCKED OPEN ORDERS VALUE IN EURO"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.y1_unblocked_open_orders_value": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Y-1 UNBLOCKED OPEN ORDERS VALUE"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.y1_total_sales_in_eur": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Y-1 TOTAL SALES in EUR"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "date.date": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Date",
    			          "ConceptualProperty": "Date"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "dim_product.brand_code": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_product",
    			          "ConceptualProperty": "Brand code"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "dim_product.brand_label": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_product",
    			          "ConceptualProperty": "Brand label"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "dim_product.sub_brand_code": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_product",
    			          "ConceptualProperty": "Sub brand code"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "dim_product.sub_brand_label": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_product",
    			          "ConceptualProperty": "Sub brand label"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "dim_product.product_code": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_product",
    			          "ConceptualProperty": "Product code"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "dim_product.axe_label": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_product",
    			          "ConceptualProperty": "Axe label"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "dim_product.sub_axe_label": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_product",
    			          "ConceptualProperty": "Sub axe label"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "dim_product.compass_code": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_product",
    			          "ConceptualProperty": "Compass code"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "dim_product.compass_product_label": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_product",
    			          "ConceptualProperty": "Compass product label"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "dim_product.compass_product_marketing_label": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_product",
    			          "ConceptualProperty": "Compass product marketing label"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "dim_sales_customer.sales_group": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_sales_customer",
    			          "ConceptualProperty": "Sales group"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "dim_sales_customer.sales_office": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_sales_customer",
    			          "ConceptualProperty": "Sales office"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "dim_sales_customer.group_division": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_sales_customer",
    			          "ConceptualProperty": "Group division"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.mtd__is_target_reached": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "MTD % IS TARGET REACHED"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.ytd_blocked_open_orders_in_units": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YTD BLOCKED OPEN ORDERS IN UNITS"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.ytd_blocked_open_orders_value": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YTD BLOCKED OPEN ORDERS VALUE"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.ytd_blocked_open_orders_value_in_eur": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YTD BLOCKED OPEN ORDERS VALUE IN EUR"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.yoy__total_sales": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YOY % TOTAL SALES"
    			        }
    			      },
    			      "State": "Generated",
    			      "Terms": [
    			        {
    			          "Total Sales YOY %": {
    			            "State": "Suggested",
    			            "Source": {
    			              "Type": "External",
    			              "Agent": "PowerBI.VisualColumnRename"
    			            },
    			            "Weight": 0.9
    			          }
    			        }
    			      ]
    			    },
    			    "measures_.yoy__total_sales_in_eur": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YOY % TOTAL SALES IN EUR"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.yoy__is_target_reached": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YOY % IS TARGET REACHED"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.yoy__cns_target_reached": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YOY % CNS TARGET REACHED"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.y1__cns_target_reached": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Y-1 % CNS TARGET REACHED"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.y1__is_target_reached": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Y-1 % IS TARGET REACHED"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.invoiced_sales": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Invoiced sales"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.invoiced_sales_in_eur": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Invoiced sales in EUR"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.conso_net_sales": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Conso net sales"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.conso_net_sales_in_eur": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Conso net sales in EUR"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.total_sales": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Total Sales"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.total_sales_eur": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Total Sales EUR"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.ytd__cns_target_reached": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YTD % CNS TARGET REACHED"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.ytd__is_target_reached": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YTD % IS TARGET REACHED"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.ytd_total_sales": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YTD TOTAL SALES"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.ytd_total_sales_in_eur": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YTD TOTAL SALES IN EUR"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.y1_invoiced_sales": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Y-1 INVOICED SALES"
    			        }
    			      },
    			      "State": "Generated",
    			      "Terms": [
    			        {
    			          "Invoiced sales Y-1": {
    			            "State": "Suggested",
    			            "Source": {
    			              "Type": "External",
    			              "Agent": "PowerBI.VisualColumnRename"
    			            },
    			            "Weight": 0.9
    			          }
    			        }
    			      ]
    			    },
    			    "measures_.yoy__invoiced_sales": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YOY % INVOICED SALES"
    			        }
    			      },
    			      "State": "Generated",
    			      "Terms": [
    			        {
    			          "Invoiced sales YOY %": {
    			            "State": "Suggested",
    			            "Source": {
    			              "Type": "External",
    			              "Agent": "PowerBI.VisualColumnRename"
    			            },
    			            "Weight": 0.9
    			          }
    			        }
    			      ]
    			    },
    			    "measures_.y1_conso_net_sales": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Y-1 CONSO NET SALES"
    			        }
    			      },
    			      "State": "Generated",
    			      "Terms": [
    			        {
    			          "Conso net sales Y-1": {
    			            "State": "Suggested",
    			            "Source": {
    			              "Type": "External",
    			              "Agent": "PowerBI.VisualColumnRename"
    			            },
    			            "Weight": 0.9
    			          }
    			        }
    			      ]
    			    },
    			    "measures_.yoy__conso_net_sales": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "YOY % CONSO NET SALES"
    			        }
    			      },
    			      "State": "Generated",
    			      "Terms": [
    			        {
    			          "Conso net sales YOY %": {
    			            "State": "Suggested",
    			            "Source": {
    			              "Type": "External",
    			              "Agent": "PowerBI.VisualColumnRename"
    			            },
    			            "Weight": 0.9
    			          }
    			        }
    			      ]
    			    },
    			    "dim_sales_customer.level0_customer_name": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_sales_customer",
    			          "ConceptualProperty": "Level0 customer name"
    			        }
    			      },
    			      "State": "Generated",
    			      "Terms": [
    			        {
    			          "Level0 customer name": {
    			            "State": "Suggested",
    			            "Source": {
    			              "Type": "External",
    			              "Agent": "PowerBI.VisualColumnRename"
    			            },
    			            "Weight": 0.9
    			          }
    			        }
    			      ]
    			    },
    			    "fact_combined.customer_sold_to": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "fact_combined",
    			          "ConceptualProperty": "customer_sold_to"
    			        }
    			      },
    			      "State": "Generated"
    			    },
    			    "measures_.invoiced_sales_n": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Invoiced sales N"
    			        }
    			      },
    			      "State": "Generated",
    			      "Terms": [
    			        {
    			          "Invoiced sales": {
    			            "State": "Suggested",
    			            "Source": {
    			              "Type": "External",
    			              "Agent": "PowerBI.VisualColumnRename"
    			            },
    			            "Weight": 0.9
    			          }
    			        }
    			      ]
    			    },
    			    "measures_.invoiced_sales_in_eur_n": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Invoiced sales in EUR N"
    			        }
    			      },
    			      "State": "Generated",
    			      "Terms": [
    			        {
    			          "Invoiced sales in EUR": {
    			            "State": "Suggested",
    			            "Source": {
    			              "Type": "External",
    			              "Agent": "PowerBI.VisualColumnRename"
    			            },
    			            "Weight": 0.9
    			          }
    			        }
    			      ]
    			    },
    			    "measures_.conso_net_sales_n": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Conso net sales N"
    			        }
    			      },
    			      "State": "Generated",
    			      "Terms": [
    			        {
    			          "Conso net sales": {
    			            "State": "Suggested",
    			            "Source": {
    			              "Type": "External",
    			              "Agent": "PowerBI.VisualColumnRename"
    			            },
    			            "Weight": 0.9
    			          }
    			        }
    			      ]
    			    },
    			    "measures_.conso_net_sales_in_eur_n": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Conso net sales in EUR N"
    			        }
    			      },
    			      "State": "Generated",
    			      "Terms": [
    			        {
    			          "Conso net sales in EUR": {
    			            "State": "Suggested",
    			            "Source": {
    			              "Type": "External",
    			              "Agent": "PowerBI.VisualColumnRename"
    			            },
    			            "Weight": 0.9
    			          }
    			        }
    			      ]
    			    },
    			    "measures_.total_sales_n": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "Measures_",
    			          "ConceptualProperty": "Total Sales N"
    			        }
    			      },
    			      "State": "Generated",
    			      "Terms": [
    			        {
    			          "Total Sales": {
    			            "State": "Suggested",
    			            "Source": {
    			              "Type": "External",
    			              "Agent": "PowerBI.VisualColumnRename"
    			            },
    			            "Weight": 0.9
    			          }
    			        }
    			      ]
    			    },
    			    "dim_sales_customer.level1_customer_name": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "dim_sales_customer",
    			          "ConceptualProperty": "Level1 customer name"
    			        }
    			      },
    			      "State": "Generated",
    			      "Terms": [
    			        {
    			          "Level1 customer name": {
    			            "State": "Suggested",
    			            "Source": {
    			              "Type": "External",
    			              "Agent": "PowerBI.VisualColumnRename"
    			            },
    			            "Weight": 0.9
    			          }
    			        }
    			      ]
    			    },
    			    "ti_table.data_analysis": {
    			      "Definition": {
    			        "Binding": {
    			          "ConceptualEntity": "TI_Table",
    			          "ConceptualProperty": "data_analysis"
    			        }
    			      },
    			      "State": "Generated",
    			      "Terms": [
    			        {
    			          "Date": {
    			            "State": "Suggested",
    			            "Source": {
    			              "Type": "External",
    			              "Agent": "PowerBI.VisualColumnRename"
    			            },
    			            "Weight": 0.9
    			          }
    			        }
    			      ]
    			    }
    			  }
    			}
    		contentType: json

- path: definition/expressions.tmdl
  payload: |+
    expression GCP_Project = "itg-neoanalytics-gbl-ww-np" meta [IsParameterQuery=true, List={"oa-data-analyticstest1-np", "itg-neoanalytics-gbl-ww-np"}, DefaultValue="oa-data-analyticstest1-np", Type="Any", IsParameterQueryRequired=true]
    	lineageTag: 80e01d7c-ca7b-468c-b5e4-bd4d0cfb58f2

    	annotation PBI_NavigationStepName = Navigation

    	annotation PBI_ResultType = Text

    expression GCP_DataSet = "neoanalytics_ds_c2_lookmlpoc_cds_eu_np" meta [IsParameterQuery=true, List={"ssbitest_ds_c2_templatecds_visible_eu_np", "neoanalytics_ds_c2_lookmlpoc_cds_eu_np"}, DefaultValue="neoanalytics_ds_c2_lookmlpoc_cds_eu_np", Type="Text", IsParameterQueryRequired=true]
    	lineageTag: 8e1ea0a2-60e9-4bf7-9a59-97b090b6c9d3

    	annotation PBI_NavigationStepName = Navigation

    	annotation PBI_ResultType = Text

    expression GCP_DataSet_Dim_NeoAnalytics = "neoanalytics_ds_c2_lookmlpoc_eu_np" meta [IsParameterQuery=true, List={"neoanalytics_ds_c2_lookmlpoc_eu_np"}, DefaultValue="neoanalytics_ds_c2_lookmlpoc_eu_np", Type="Text", IsParameterQueryRequired=true]
    	lineageTag: 1fe09317-93c9-4807-bc10-fcc328354dc3

    	annotation PBI_NavigationStepName = Navigation

    	annotation PBI_ResultType = Text

    expression PRM_fact_sellin = "fact_turnover_combined_secured_11b" meta [IsParameterQuery=true, List={"fact_turnover_combined_secured_11b", "fact_turnover_combined_secured_11o", "fact_turnover_combined_secured_35", "fact_turnover_combined_secured_r11"}, DefaultValue="fact_turnover_combined_secured_11b", Type="Text", IsParameterQueryRequired=true]
    	lineageTag: 3ddba414-96cc-4f29-943f-4c62fcf7ffce
    	parameterValuesColumn: Selin.Combined

    	annotation PBI_NavigationStepName = Navigation

    	annotation PBI_ResultType = Text

    expression PRM_fact_salestarget = "fact_salestarget_secured_11b" meta [IsParameterQuery=true, List={"fact_salestarget_secured_11b", "fact_salestarget_secured_11o", "fact_salestarget_secured_35", "fact_salestarget_secured_r11"}, DefaultValue="fact_salestarget_secured_11b", Type="Text", IsParameterQueryRequired=true]
    	lineageTag: 732495fb-26b5-4320-8408-17f9124733b3

    	annotation PBI_ResultType = Text

    expression PRM_fact_porffolio = "fact_portfolio_secured_11b" meta [IsParameterQuery=true, List={"fact_portfolio_secured_11b", "fact_portfolio_secured_11o", "fact_portfolio_secured_35", "fact_portfolio_secured_r11"}, DefaultValue="fact_portfolio_secured_11b", Type="Text", IsParameterQueryRequired=true]
    	lineageTag: df4219d1-bbc8-4ad0-be04-73aba1a85085

    	annotation PBI_NavigationStepName = Navigation

    	annotation PBI_ResultType = Text

- path: definition/model.tmdl
  payload: |+
    model Model
    	culture: en-US
    	defaultPowerBIDataSourceVersion: powerBI_V3
    	sourceQueryCulture: en-US
    	dataAccessOptions
    		legacyRedirects
    		returnErrorValuesAsNull

    annotation PBI_QueryOrder = ["fact_combined","dim_axis","dim_product","dim_sales_customer","dim_sales_product","dim_signature","GCP_Project","GCP_DataSet","GCP_DataSet_Dim_NeoAnalytics","dim_hub","customGroup","TI_Table","PRM_fact_sellin","PRM_fact_salestarget","PRM_fact_porffolio","Selin"]

    annotation __PBI_TimeIntelligenceEnabled = 1

    annotation PBIDesktopVersion = 2.145.1457.0 (25.07)+6e87ffa743c5aa106a85a0b5e383d76d522045ba

    ref table DateTableTemplate_6ee25a60-95ad-4112-a624-f7a3c1e4f904
    ref table Measures_
    ref table Date
    ref table LocalDateTable_bc1da608-328f-482f-89bd-aa0b143b50f1
    ref table dim_axis
    ref table dim_product
    ref table dim_sales_customer
    ref table dim_sales_product
    ref table dim_signature
    ref table 'Dimension Selection'
    ref table 'KPI Selection'
    ref table dim_hub
    ref table fact_combined
    ref table KPI
    ref table customGroup
    ref table TI_Table
    ref table LocalDateTable_f992abc6-6c6f-467b-915f-f7ab15fee947
    ref table LocalDateTable_a10507c8-3a5a-4373-a663-4cfa3ae454b6
    ref table Selin

    ref cultureInfo en-US

- path: definition/database.tmdl
  payload: |+
    database
    	compatibilityLevel: 1567

- path: definition.pbism
  payload: |-
    {
      "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
      "version": "4.2",
      "settings": {}
    }
- path: .pbi/editorSettings.json
  payload: |-
    {
      "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/editorSettings/1.0.0/schema.json",
      "autodetectRelationships": true,
      "parallelQueryLoading": true,
      "typeDetectionEnabled": true,
      "relationshipImportEnabled": true,
      "shouldNotifyUserOfNameConflictResolution": true
    }
- path: .platform
  payload: |-
    {
      "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
      "metadata": {
        "type": "SemanticModel",
        "displayName": "PBIModel_NewConnector_Combined_Optimized_V1"
      },
      "config": {
        "version": "2.0",
        "logicalId": "00000000-0000-0000-0000-000000000000"
      }
    }

## Protocol

1. With the provided schema, generate the DAX query according to the business question.

NB: If you don't know ho to answer the question, you can ask me for more information.

2. Run the Query using PowerBI API

```bash
ACCESS_TOKEN="$(az account get-access-token --resource https://analysis.windows.net/powerbi/api|jq -r .accessToken)";
curl -s -L -v -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -X POST https://api.powerbi.com/v1.0/myorg/datasets/f69d81f2-cb74-40fd-9cbe-82eaeed99b3d/executeQueries -d '{"queries":[{"query": "<DAX CODE GENERATED>"}],"serializerSettings":{"includeNulls":true}}'
```

3. Return the results of the API call.
