function onOpen() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var menus = [
    {name: "KintoneAppName" ,functionName: "setContactRCVKintoneInfoData" }
  ];
  ss.addMenu("カスタムメニュー", menus);
  return;
}


function setContactRCVKintoneInfoData() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var SheetName = '';
  var KintoneAppName = '';
  
  // 指定シートへデータを書き出し
  var sheet = ss.getSheetByName(sheetname);
  var queryOffset = 0;
  var baseQuery = 'XXXX order by date desc limit 500 offset ';
  var records = getKintoneData(KintoneAppName, baseQuery);
  var datas = reshepeContactRCVKintoneRecords(records);
  Logger.log(datas);
  sheet.getRange(2, 1, sheet.getLastRow(), sheet.getLastColumn()).clearContent();
  sheet.getRange(2, 1, datas.length, datas[0].length).setValues(datas);

  var funcValues = [[
    "=ARRAYFORMULA(IF(B2:B=\"\",\"\",text(B2:B,\"yyyy\/mm\")))",
  ]];
  sheet.getRange(2, 6,1,funcValues[0].length).setValues(funcValues);
  return;
}

function getKintoneData(appName, baseQuery) {
  var tokenSheet = SpreadsheetApp.openByUrl("https://docs.google.com/spreadsheets/d/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/edit#gid=0");
  var token = tokenSheet.getRange('B2').getValue();
  var KintoneAppName = '';

  var subdomain = "xxxxxxx";
  var apps = {
    KintoneAppName : { appid: xxx, name: KintoneAppName, token: token }
  };
  var kintone_manager = new KintoneManager.KintoneManager(subdomain, apps);
  
  var queryOffset = 0;
  var records = [];
  
  do {
    var query = baseQuery + queryOffset
    var response = kintone_manager.search(appName, query);
    // ステータスコード
    // 成功すれば200になる
    var code = response.getResponseCode();
    var content = JSON.parse(response.getContentText());
    records = records.concat(content.records);
    queryOffset += 500; 
    // レコードの配列が取得できる。
  } while (content.records.length == 500)
  
  return records;
}

// KintoneAppデータ整形
function reshepeContactRCVKintoneRecords(records) {
  var datas = [];
  for (var i in records) {
    var data = [];
    data.push(
      records[i].fieldName.value
    );
    datas.push(data);
  }
  Logger.log(datas);
  
  return datas;
}

// チェックボックスの場合この関数を使う
function reshapeCheckBoxField(values) {
  if (values.length == 0) return '';
  var rtn = '';
  values.forEach(function(value) {
    rtn += ',' + value;
  });
  return rtn.substr(1);
}

// ユーザー選択の場合この関数を使う
function reshapeUserSelectField(values) {
  if (values.length == 0) return '';
  var rtn = '';
  values.forEach(function(value) {
    rtn += ',' + value.name;
  });
  return rtn.substr(1);
}