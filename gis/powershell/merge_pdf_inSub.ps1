    $pdftk = "C:\Program Files (x86)\PDFtk\bin\pdftk.exe"
    $RootFolder = "Z:\BMGFGRID\ScienceData$\mheaton\Documents\DRC_m4h_january22_20220126\A2_IT_KL\KWILU"
    Get-ChildItem -r -include *.pdf | group DirectoryName | % {& $PDFtk $_.group CAT OUTPUT "$($_.Name | Split-Path -Parent)\$($_.Name | Split-Path -Leaf)_merged.pdf"}