$folder = 'D:\GRID\ZMB\Cartography\ZMB_EPI_COVAX_december_20211207\pdf_output\20220923_hfca\'

Get-ChildItem "$folder/*.pdf" |
    ForEach-Object{
        $target = ($_.Name -split '_')[3]
        If(!(test-path $folder\$target))
            {
            New-Item -ItemType Directory -Force -Path $folder\$target
            }
        }


Get-ChildItem "$folder/*.pdf" |
    ForEach-Object{
        $target = ($_.Name -split '_')[3]
        $_ | Move-Item -Destination $folder\$target
    }

