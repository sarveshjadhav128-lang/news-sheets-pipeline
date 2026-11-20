function appendNewsRows(rows) {
  if (!rows) {
    rows = [
      ["Sample Streaming Update", "1h ago", "https://example.com/news-sample"]
    ];
  }

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName("news") || ss.insertSheet("news");

  if (sheet.getLastRow() === 0) {
    sheet.appendRow(["headline", "date", "url"]);
  }

  const startRow = sheet.getLastRow() + 1;
  sheet.getRange(startRow, 1, rows.length, 3).setValues(rows);
}

function sendPipelineSummaryEmail() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName("news");
  const totalRows = sheet ? Math.max(sheet.getLastRow() - 1, 0) : 0;
  const userEmail = Session.getActiveUser().getEmail();

  if (userEmail) {
    MailApp.sendEmail(
      userEmail,
      "News Pipeline Summary",
      "Total scraped headlines in sheet: " + totalRows + "\nSpreadsheet: " + ss.getUrl()
    );
  }
}