Param(
    [parameter(ValueFromRemainingArguments=$true)]
    [string]
    $docPaths, 
    [parameter(ValueFromPipelineByPropertyName=$true)]
    [switch][bool]
    $Replace,
    [switch][bool]
    $Register, # 註冊右鍵選單
    [switch][bool]
    $Unregister # 取消註冊右鍵選單
)
$ErrorActionPreference = "STOP"
function getDocxShellKeyPath() {
    # 由 HKEY_CLASSES_ROOT\.docx 取得 Word 文件對應的機碼名稱(如：Word.Document.12)
    $docxKeyName = [Microsoft.Win32.Registry]::ClassesRoot.OpenSubKey(".docx").GetValue('')
    return "SOFTWARE\Classes\$docxKeyName\shell\ToPdf"   
}
if ($Unregister) {
    $regPath = getDocxShellKeyPath
    $reg = [Microsoft.Win32.Registry]::CurrentUser
    $key = $reg.OpenSubKey($regPath, $true)
    if ($key) { $reg.DeleteSubKeyTree($regPath) }
    return
}
if ($Register) {
    $regPath = getDocxShellKeyPath
    $reg = [Microsoft.Win32.Registry]::CurrentUser
    $key = $reg.OpenSubKey($regPath, $true)
    if (-not $key) { $key = $reg.CreateSubKey($regPath) }
    $key.SetValue("", "Save as PDF (English file name only)")
    $key = $reg.OpenSubKey("$regPath\command", $true)
    if (-not $key) { $key = $reg.CreateSubKey("$regPath\command") }
    $key.SetValue("", "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command `"$PSScriptRoot\Docs2Pdf.ps1 %1`"")
    return
}

if (!$docPaths) {
    Write-Host "Please set the convert word file path "
    return
}

try 
{
    $doc = New-Object -ComObject Word.Application
    $doc.Visible = $true # 顯示 UI，方便使用者了解處理進度、輸入密碼等
    Get-Item $docPaths | ForEach-Object {
        $path = $_.FullName
        Write-Host "Opening $path..."
        try {
            $doc.Documents.Open($path) | Out-Null
            #read-host “Press ENTER to continue...”
            $savePath = [System.IO.Path]::ChangeExtension($path, ".pdf")
            #read-host “Press ENTER to continue...”
            # https://docs.microsoft.com/en-us/office/vba/api/word.wdsaveformat
            # WdSaveFormat.wdFormatPDF = 17
            $doc.ActiveDocument.SaveAs2($savePath, 17)

            $doc.ActiveDocument.Close()
            if ($replace) {
                Remove-Item $path                
            }
        }
        catch {Write-Host "Error - $path" -ForegroundColor Red
        }
    }
}
finally 
{
    $doc.Quit()
}