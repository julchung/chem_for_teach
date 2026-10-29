import processing.video.*;
import javax.swing.JOptionPane;

Capture cam;
PImage img;
PImage camBuffer; // 新增：持久化的快照緩衝，免於頻繁 new PImage

Button btnImage, btnCamera, btnSnapshot, btnCalib1, btnCalib2, btnResetCalib, btnExport, btnScreenshot;
boolean isCameraFrozen = false; // 相機暫停（拍照模式）
PFont font;

float crossX = -1; // -1 表示尚未初始化
float lineScanY = -1; // 新增：掃描取的水平高度
boolean isCameraActive = false;
int[] intensityData;

// ==== 相機下拉選單 ====
String[] cameraList = new String[0];
int selectedCameraIndex = 0;
boolean dropdownOpen = false;
float ddX, ddY, ddW, ddH; // 下拉選單位置尺寸

float calibPixel1 = -1;
float calibWave1 = -1;
float calibScanY1 = -1; // 新增：校正點1所在的Y高度
float calibPixel2 = -1;
float calibWave2 = -1;
float calibScanY2 = -1; // 新增：校正點2所在的Y高度
boolean isCalibrated = false;

void setup() {
  size(1200, 800);
  surface.setResizable(true); // 視窗大小可調整
  
  try {
    font = createFont("Microsoft JhengHei", 15);
  } catch (Exception e) {
    font = createFont("SansSerif", 15); // 回退方案
  }
  textFont(font);
  
  // 取得可用相機清單
  try {
    String[] cams = Capture.list();
    if (cams != null && cams.length > 0) {
      cameraList = cams;
    } else {
      cameraList = new String[]{"(無可用相機)"};
    }
  } catch (Exception e) {
    cameraList = new String[]{"(無法取得相機清單)"};
  }
  
  btnImage = new Button("開啟照片", 0, 0, 20);
  btnCamera = new Button("開啟相機", 0, 0, 20);
  btnSnapshot = new Button("拍照", 0, 0, 20);
  btnCalib1 = new Button("設定波長 1", 0, 0, 20);
  btnCalib2 = new Button("設定波長 2", 0, 0, 20);
  btnResetCalib = new Button("重設波長", 0, 0, 20);
  btnExport = new Button("匯出資料(CSV)", 0, 0, 20);
  btnScreenshot = new Button("儲存圖表截圖", 0, 0, 20);
}

void draw() {
  // 1. 防止調整視窗或最大化瞬時產生非法大小導致繪圖崩潰
  if (width <= 0 || height <= 0 || width < 200 || height < 150) {
    background(240);
    fill(0);
    textAlign(CENTER, CENTER);
    text("視窗大小不合法或過小...", width / 2, height / 2);
    return;
  }

  background(240);
  
  float leftWidth = width * 5.0 / 6.0;
  float rightWidth = width - leftWidth;
  float topHeight = height / 2.0;
  float bottomHeight = height - topHeight;
  
  // ==== 右方工具列 ====
  fill(255);
  noStroke();
  rect(leftWidth, 0, rightWidth, height);
  
  float btnW = min(195, rightWidth - 20);
  float btnH = 40;
  float ddItemH = 28; // 下拉選項高度
  
  // ---- 開啟照片區 ----
  float sectionFileY = 20;
  btnImage.x = leftWidth + (rightWidth - btnW) / 2;
  btnImage.y = sectionFileY;
  btnImage.w = max(10, btnW);
  btnImage.h = btnH;
  btnImage.display();

  // ---- 分隔線 ----
  float sepY1 = sectionFileY + btnH + 14;
  stroke(180);
  strokeWeight(1);
  line(leftWidth + 10, sepY1, leftWidth + rightWidth - 10, sepY1);
  noStroke();

  // ---- 開啟相機區 ----
  float sectionCamY = sepY1 + 12;

  // 相機選擇下拉選單
  ddW = max(10, btnW);
  ddH = btnH;
  ddX = leftWidth + (rightWidth - btnW) / 2;
  ddY = sectionCamY;

  // 繪製下拉選單主體
  fill(230);
  stroke(120);
  strokeWeight(1);
  rect(ddX, ddY, ddW, ddH, 4);
  fill(0);
  textAlign(LEFT, CENTER);
  textSize(15);
  String ddLabel = (cameraList.length > 0) ? shortCamName(cameraList[selectedCameraIndex]) : "(無相機)";
  text(ddLabel, ddX + 8, ddY + ddH / 2);
  // 繪製箭頭
  fill(80);
  noStroke();
  float arrowX = ddX + ddW - 18;
  float arrowY = ddY + ddH / 2;
  triangle(arrowX, arrowY - 5, arrowX + 10, arrowY - 5, arrowX + 5, arrowY + 5);

  // 下拉展開清單（繪製在最上層，最後繪製）
  // 這裡先記錄位置，稍後在 draw() 末尾繪製

  btnCamera.x = leftWidth + (rightWidth - btnW) / 2;
  btnCamera.y = sectionCamY + ddH + 8;
  btnCamera.w = max(10, btnW);
  btnCamera.h = btnH;

  btnSnapshot.x = leftWidth + (rightWidth - btnW) / 2;
  btnSnapshot.y = sectionCamY + ddH + 8 + (btnH + 8);
  btnSnapshot.w = max(10, btnW);
  btnSnapshot.h = btnH;
  
  btnExport.x = leftWidth + (rightWidth - btnW) / 2;
  btnExport.y = sectionCamY + ddH + 8 + (btnH + 8) * 2;
  btnExport.w = max(10, btnW);
  btnExport.h = btnH;
  
  btnScreenshot.x = leftWidth + (rightWidth - btnW) / 2;
  btnScreenshot.y = sectionCamY + ddH + 8 + (btnH + 8) * 3;
  btnScreenshot.w = max(10, btnW);
  btnScreenshot.h = btnH;

  float bottomStartY = height - (btnH + 10) * 3 - 30;

  btnCalib1.x = leftWidth + (rightWidth - btnW) / 2;
  btnCalib1.y = bottomStartY;
  btnCalib1.w = max(10, btnW);
  btnCalib1.h = btnH;
  
  btnCalib2.x = leftWidth + (rightWidth - btnW) / 2;
  btnCalib2.y = bottomStartY + btnH + 10;
  btnCalib2.w = max(10, btnW);
  btnCalib2.h = btnH;
  
  btnResetCalib.x = leftWidth + (rightWidth - btnW) / 2;
  btnResetCalib.y = bottomStartY + (btnH + 10) * 2;
  btnResetCalib.w = max(10, btnW);
  btnResetCalib.h = btnH;
  
  btnCalib1.label = (calibPixel1 >= 0) ? "波長1: " + nf(calibWave1, 0, 1) : "設定波長 1";
  btnCalib2.label = (calibPixel2 >= 0) ? "波長2: " + nf(calibWave2, 0, 1) : "設定波長 2";
  btnCamera.label = isCameraFrozen ? "開啟相機" : (isCameraActive ? "關閉相機" : "開啟相機");
  btnSnapshot.label = isCameraFrozen ? "恢復即時" : "拍照";
  
  btnCamera.display();
  btnSnapshot.display();
  btnCalib1.display();
  btnCalib2.display();
  btnResetCalib.display();
  btnExport.display();
  btnScreenshot.display();

  // 下拉展開清單（最後繪製，蓋在其他元件之上）
  if (dropdownOpen && cameraList.length > 0) {
    float listY = ddY + ddH;
    for (int i = 0; i < cameraList.length; i++) {
      if (i == selectedCameraIndex) {
        fill(180, 210, 255);
      } else if (mouseX >= ddX && mouseX <= ddX + ddW && mouseY >= listY + i * ddItemH && mouseY <= listY + (i + 1) * ddItemH) {
        fill(220, 235, 255);
      } else {
        fill(245);
      }
      stroke(180);
      strokeWeight(1);
      rect(ddX, listY + i * ddItemH, ddW, ddItemH);
      fill(0);
      textAlign(LEFT, CENTER);
      textSize(13);
      text(shortCamName(cameraList[i]), ddX + 6, listY + i * ddItemH + ddItemH / 2);
    }
  }
  
  // ==== 左方半部背景 ====
  fill(220);
  rect(0, 0, leftWidth, topHeight);
  fill(240);
  rect(0, topHeight, leftWidth, bottomHeight);
  
  float imgX = 20;
  float imgY = 20;
  float imgW = leftWidth - 40;
  float imgH = topHeight - 40;
  
  PImage src = null;
  try {
    if (isCameraActive && cam != null) {
      if (!isCameraFrozen && cam.available()) {
        cam.read();
        
        // 優化：避免 cam.get() 頻繁分配記憶體
        if (camBuffer == null || camBuffer.width != cam.width || camBuffer.height != cam.height) {
          camBuffer = new PImage(cam.width, cam.height, RGB);
        }
        camBuffer.copy(cam, 0, 0, cam.width, cam.height, 0, 0, cam.width, cam.height);
      }
      
      if (camBuffer != null && camBuffer.width > 0) {
        src = camBuffer;
      }
    } else if (!isCameraActive && img != null) {
      src = img;
    }
  } catch (Exception e) {
    println("擷取影像發生錯誤：" + e.getMessage());
  }
  
  if (src != null && src.width > 0 && src.height > 0 && imgW > 0 && imgH > 0) {
    int sw = src.width;
    int sh = src.height;
    
    // 初始化 crossX 和 lineScanY (置中)
    if (crossX < 0) {
      crossX = sw / 2.0;
    }
    crossX = constrain(crossX, 0, sw - 1);
    
    // 初始化 lineScanY (置中)
    if (lineScanY < 0) {
      lineScanY = sh / 2.0;
    }
    lineScanY = constrain(lineScanY, 0, sh - 1);
    
    // ==== 左上方：繪製影像（可縮放）====
    image(src, imgX, imgY, imgW, imgH);
    
    // 影像水平掃描線
    float absLineY = map(lineScanY, 0, sh - 1, imgY, imgY + imgH);
    stroke(255, 0, 0);
    line(imgX, absLineY, imgX + imgW, absLineY);
    
    // 繪製校正標記 (小圓圈)
    strokeWeight(2);
    if (calibPixel1 >= 0 && calibScanY1 >= 0) {
      float markerX = map(calibPixel1, 0, sw - 1, imgX, imgX + imgW);
      float markerY = map(calibScanY1, 0, sh - 1, imgY, imgY + imgH);
      noFill();
      stroke(0, 255, 255); // 青色標記
      ellipse(markerX, markerY, 8, 8);
    }
    if (calibPixel2 >= 0 && calibScanY2 >= 0) {
      float markerX = map(calibPixel2, 0, sw - 1, imgX, imgX + imgW);
      float markerY = map(calibScanY2, 0, sh - 1, imgY, imgY + imgH);
      noFill();
      stroke(255, 255, 0); // 黃色標記
      ellipse(markerX, markerY, 8, 8);
    }
    strokeWeight(1);
    
    // 影像上的紅色十字 (顯示在當前掃描線上)
    float absCrossX = map(crossX, 0, sw - 1, imgX, imgX + imgW);
    stroke(255, 0, 0);
    line(absCrossX - 10, absLineY, absCrossX + 10, absLineY);
    line(absCrossX, absLineY - 10, absCrossX, absLineY + 10);
    stroke(0);
    
    // 擷取水平線各像素強度
    try {
      src.loadPixels();
      int sy = round(lineScanY);
      sy = constrain(sy, 0, sh - 1);
      
      // 避免每一幀 new 陣列
      if (intensityData == null || intensityData.length != sw) {
        intensityData = new int[sw];
      }
      
      for (int i = 0; i < sw; i++) {
         int idx = sy * sw + i;
         if (idx >= 0 && idx < src.pixels.length) {
           intensityData[i] = (int)brightness(src.pixels[idx]);
         } else {
           intensityData[i] = 0;
         }
      }
    } catch (Exception e) {
      println("取得像素時發生錯誤：" + e.getMessage());
    }
    
    // ==== 左下方：即時呈現強度圖譜 ====
    float gx = 50;
    float gy = topHeight + 20;
    float gw = leftWidth - 100;
    float gh = bottomHeight - 60;
    
    // 各種安全條件，防禦在視窗拉扯或放大過程中的數學錯誤
    if (gw > 1 && gh > 1) {
      drawAxes(gx, gy, gw, gh, sw);
      
      stroke(0);
      noFill();
      beginShape();
      for (int i = 0; i < sw; i++) {
        float x = map(i, 0, sw - 1, gx, gx + gw);
        float y = map(intensityData[i], 0, 255, gy + gh, gy);
        vertex(x, y);
      }
      endShape();
      
      // 折線圖中的紅色十字
      int ix = (int)crossX;
      if (ix >= 0 && ix < intensityData.length) {
        stroke(255, 0, 0);
        float gCrossX = map(crossX, 0, sw - 1, gx, gx + gw);
        float gCrossY = map((float)intensityData[ix], 0, 255, gy + gh, gy);
        line(gCrossX - 10, gCrossY, gCrossX + 10, gCrossY);
        line(gCrossX, gCrossY - 10, gCrossX, gCrossY + 10);
        
        // 顯示座標
        fill(255, 0, 0);
        textSize(30);
        textAlign(LEFT, TOP);
        String xCoordLabel;
        if (isCalibrated) {
          float wLabel = map(crossX, calibPixel1, calibPixel2, calibWave1, calibWave2);
          xCoordLabel = nf(wLabel, 0, 1) + " nm";
        } else {
          xCoordLabel = nf(crossX, 0, 1);
        }
        text("(" + xCoordLabel + ", " + intensityData[ix] + ")", gx, gy + 10);
      }
      stroke(0);
    }
  }
}

void drawAxes(float gx, float gy, float gw, float gh, int sw) {
  stroke(0);
  fill(0);
  textSize(12);
  
  // X, Y 軸線
  line(gx, gy + gh, gx + gw, gy + gh);
  line(gx, gy + gh, gx, gy);
  
  // Y 軸刻度
  textAlign(RIGHT, CENTER);
  for (int i = 0; i <= 255; i += 51) {
    float y = map(i, 0, 255, gy + gh, gy);
    line(gx - 5, y, gx, y);
    text(i, gx - 8, y);
  }
  
  // X 軸刻度
  textAlign(CENTER, TOP);
  int xStep = max(1, sw / 10);
  for (int i = 0; i < sw; i += xStep) {
    float x = map(i, 0, sw - 1, gx, gx + gw);
    line(x, gy + gh, x, gy + gh + 5);
    
    String xLabel;
    if (isCalibrated) {
      float w = map(i, calibPixel1, calibPixel2, calibWave1, calibWave2);
      xLabel = nf(w, 0, 1);
    } else {
      xLabel = String.valueOf(i);
    }
    text(xLabel, x, gy + gh + 8);
  }
}

void mousePressed() {
  // 相機下拉選單處理
  float ddItemH = 28;
  if (dropdownOpen && cameraList.length > 0) {
    float listY = ddY + ddH;
    for (int i = 0; i < cameraList.length; i++) {
      if (mouseX >= ddX && mouseX <= ddX + ddW &&
          mouseY >= listY + i * ddItemH && mouseY <= listY + (i + 1) * ddItemH) {
        selectedCameraIndex = i;
        dropdownOpen = false;
        return;
      }
    }
    // 點擊清單外部關閉
    dropdownOpen = false;
    return;
  }
  
  // 點擊下拉選單主體開啟/關閉
  if (mouseX >= ddX && mouseX <= ddX + ddW && mouseY >= ddY && mouseY <= ddY + ddH) {
    dropdownOpen = !dropdownOpen;
    return;
  }

  if (btnImage.isClicked(mouseX, mouseY)) {
    try {
      selectInput("選擇圖片", "fileSelected");
    } catch (Exception e) {
      println("檔案選擇器開啟失敗");
    }
  } else if (btnCamera.isClicked(mouseX, mouseY)) {
    if (isCameraActive) {
      // 關閉相機
      if (cam != null) {
        cam.stop();
        cam = null;
      }
      isCameraActive = false;
      isCameraFrozen = false;
      camBuffer = null;
    } else {
      startCamera();
    }
  } else if (btnSnapshot.isClicked(mouseX, mouseY)) {
    if (isCameraActive) {
      isCameraFrozen = !isCameraFrozen;
    }
  } else if (btnCalib1.isClicked(mouseX, mouseY)) {
    if (crossX >= 0) {
      String input = JOptionPane.showInputDialog("請輸入目前十字位置的波長 (nm):\n(目前像素位置: " + nf(crossX, 0, 1) + ")");
      if (input != null && !input.trim().isEmpty()) {
        try {
          calibWave1 = Float.parseFloat(input.trim());
          calibPixel1 = crossX;
          calibScanY1 = lineScanY;
          checkCalibration();
        } catch (NumberFormatException e) {
          JOptionPane.showMessageDialog(null, "請輸入有效的數字！");
        }
      }
    }
  } else if (btnCalib2.isClicked(mouseX, mouseY)) {
    if (crossX >= 0) {
      String input = JOptionPane.showInputDialog("請輸入目前十字位置的波長 (nm):\n(目前像素位置: " + nf(crossX, 0, 1) + ")");
      if (input != null && !input.trim().isEmpty()) {
        try {
          calibWave2 = Float.parseFloat(input.trim());
          calibPixel2 = crossX;
          calibScanY2 = lineScanY;
          checkCalibration();
        } catch (NumberFormatException e) {
          JOptionPane.showMessageDialog(null, "請輸入有效的數字！");
        }
      }
    }
  } else if (btnResetCalib.isClicked(mouseX, mouseY)) {
    calibPixel1 = -1;
    calibScanY1 = -1;
    calibPixel2 = -1;
    calibScanY2 = -1;
    isCalibrated = false;
  } else if (btnExport.isClicked(mouseX, mouseY)) {
    if (isCalibrated && intensityData != null) {
      selectOutput("匯出波長與強度數據 (CSV)", "fileSelectedExport");
    } else if (!isCalibrated) {
      JOptionPane.showMessageDialog(null, "請先完成兩點波長校正，才能匯出帶有波長的數據！");
    } else {
      JOptionPane.showMessageDialog(null, "沒有可匯出的數據！");
    }
  } else if (btnScreenshot.isClicked(mouseX, mouseY)) {
    selectOutput("儲存螢幕截圖", "fileSelectedScreenshot");
  } else {
    // 點擊圖譜區域時，移動紅色十字游標
    float leftWidth = width * 5.0 / 6.0;
    float topHeight = height / 2.0;
    float bottomHeight = height - topHeight;
    float gx = 50;
    float gy = topHeight + 20;
    float gw = leftWidth - 100;
    float gh = bottomHeight - 60;
    
    PImage src = null;
    if (isCameraActive && camBuffer != null) src = camBuffer;
    else if (!isCameraActive && img != null) src = img;
    
    if (src != null && mouseX >= gx && mouseX <= gx + gw && mouseY >= gy && mouseY <= gy + gh) {
      int sw = src.width;
      float clickedImgX = map(mouseX, gx, gx + gw, 0, sw - 1);
      crossX = constrain(clickedImgX, 0, sw - 1);
    }
  }
}

void fileSelectedExport(File selection) {
  if (selection != null) {
    String path = selection.getAbsolutePath();
    if (!path.toLowerCase().endsWith(".csv")) {
      path += ".csv";
    }
    PrintWriter output = createWriter(path);
    output.println("Wavelength(nm),Intensity");
    
    int sw = intensityData.length;
    for (int i = 0; i < sw; i++) {
        float w = map(i, calibPixel1, calibPixel2, calibWave1, calibWave2);
        if (w >= 290 && w <= 800) {
            output.println(nf(w, 0, 2) + "," + intensityData[i]);
        }
    }
    output.flush();
    output.close();
    JOptionPane.showMessageDialog(null, "資料匯出成功：\n" + path);
  }
}

void fileSelectedScreenshot(File selection) {
  if (selection != null) {
    String path = selection.getAbsolutePath();
    if (!path.toLowerCase().endsWith(".png")) {
      path += ".png";
    }
    
    if (isCalibrated && intensityData != null && intensityData.length > 0) {
      int sw = intensityData.length;
      float w_per_pixel = (calibWave2 - calibWave1) / (calibPixel2 - calibPixel1);
      float i_290 = calibPixel1 + (290 - calibWave1) / w_per_pixel;
      float i_850 = calibPixel1 + (850 - calibWave1) / w_per_pixel;
      
      int startI = round(min(i_290, i_850));
      int endI = round(max(i_290, i_850));
      
      startI = constrain(startI, 0, sw - 1);
      endI = constrain(endI, 0, sw - 1);
      
      if (startI < endI) {
        int cropWidth = endI - startI + 1;
        
        PImage src = null;
        if (isCameraActive && camBuffer != null && camBuffer.width > 0) {
          src = camBuffer;
        } else if (!isCameraActive && img != null) {
          src = img;
        }
        
        if (src != null) {
          int outW = max(cropWidth, 800);
          int graphH = 300;
          
          int sy = round(lineScanY);
          int cropY = max(0, sy - 25);
          int cropBottom = min(src.height, sy + 25);
          int cropHeight = cropBottom - cropY;
          
          float gx = 50;
          float gw = outW - 80;
          
          float scaleRatio = gw / cropWidth;
          int scaledImgH = round(cropHeight * scaleRatio);
          int outH = graphH + scaledImgH + 60; 
          
          PGraphics pg = createGraphics(outW, outH);
          pg.beginDraw();
          pg.background(255);
          if (font != null) {
            pg.textFont(font);
          }
          
          float gy = 20;
          float gh = graphH - 40;
          
          pg.stroke(0);
          pg.fill(0);
          pg.textSize(12);
          pg.line(gx, gy + gh, gx + gw, gy + gh); 
          pg.line(gx, gy + gh, gx, gy); 
          
          pg.textAlign(RIGHT, CENTER);
          for (int i = 0; i <= 255; i += 51) {
            float y = map(i, 0, 255, gy + gh, gy);
            pg.line(gx - 5, y, gx, y);
            pg.text(String.valueOf(i), gx - 8, y);
          }
          
          pg.textAlign(CENTER, TOP);
          float start_w = calibWave1 + (startI - calibPixel1) * w_per_pixel;
          float end_w = calibWave1 + (endI - calibPixel1) * w_per_pixel;
          
          float w_min = min(start_w, end_w);
          float w_max = max(start_w, end_w);
          
          int start_mark = ceil(w_min / 50.0f) * 50;
          for (int w = start_mark; w <= w_max; w += 50) {
            float pixel_i = calibPixel1 + (w - calibWave1) / w_per_pixel;
            if (pixel_i >= startI && pixel_i <= endI) {
              float x = map(pixel_i, startI, endI, gx, gx + gw);
              pg.line(x, gy + gh, x, gy + gh + 5);
              pg.text(String.valueOf(w), x, gy + gh + 8);
            }
          }
          
          pg.text(nf(start_w, 0, 1) + " nm", gx, gy + gh + 20);
          pg.text(nf(end_w, 0, 1) + " nm", gx + gw, gy + gh + 20);
          
          pg.noFill();
          pg.stroke(0);
          pg.strokeWeight(2);
          pg.beginShape();
          for (int i = startI; i <= endI; i++) {
            float x = map(i, startI, endI, gx, gx + gw);
            float y = map(intensityData[i], 0, 255, gy + gh, gy);
            pg.vertex(x, y);
          }
          pg.endShape();
          pg.strokeWeight(1);
          
          float imgDrawX = gx;
          float imgDrawY = graphH + 20;
          float imgDrawW = gw;
          float imgDrawH = scaledImgH;
          
          PImage croppedImg = src.get(startI, cropY, cropWidth, cropHeight);
          pg.image(croppedImg, imgDrawX, imgDrawY, imgDrawW, imgDrawH);
          
          float lineY = imgDrawY + imgDrawH / 2.0f;
          pg.stroke(255, 0, 0);
          pg.line(imgDrawX, lineY, imgDrawX + imgDrawW, lineY);
          
          pg.endDraw();
          pg.save(path);
          JOptionPane.showMessageDialog(null, "已成功儲存 290~850 nm 區間截圖：\n" + path);
          return;
        }
      }
    }
    
    saveFrame(path);
    JOptionPane.showMessageDialog(null, "截圖儲存成功(全畫面)：\n" + path);
  }
}

void checkCalibration() {
  if (calibPixel1 >= 0 && calibPixel2 >= 0 && calibPixel1 != calibPixel2) {
    isCalibrated = true;
  } else {
    isCalibrated = false;
  }
}

void keyPressed() {
  if (keyCode == RIGHT) {
    crossX += 0.5;
  } else if (keyCode == LEFT) {
    crossX -= 0.5;
  } else if (keyCode == UP) {
    lineScanY -= 1.0;
  } else if (keyCode == DOWN) {
    lineScanY += 1.0;
  }
}

void fileSelected(File selection) {
  if (selection != null) {
    img = loadImage(selection.getAbsolutePath());
    isCameraActive = false;
    if (cam != null) {
      cam.stop();
      cam = null;
    }
    camBuffer = null; 
    crossX = -1; 
  }
}

void startCamera() {
  try {
    if (cameraList == null || cameraList.length == 0 || cameraList[0].startsWith("(")) {
      println("無可用相機");
      return;
    }
    
    int camIdx = constrain(selectedCameraIndex, 0, cameraList.length - 1);
    
    isCameraActive = true;
    isCameraFrozen = false; // 重置拍照狀態
    img = null;
    if (cam != null) {
      cam.stop();
    }
    
    cam = new Capture(this, cameraList[camIdx]);
    cam.start();
    crossX = -1;
  } catch (Exception e) {
    println("相機啟動失敗：" + e.getMessage());
  }
}

// 縮短相機名稱顯示（避免太長）
String shortCamName(String name) {
  if (name == null) return "";
  // 取最後一個 '/' 或 '\\' 或逗號後的部分
  int idx = max(name.lastIndexOf('/'), name.lastIndexOf('\\'));
  String short_name = (idx >= 0) ? name.substring(idx + 1) : name;
  // 如果還是很長，截斷
  if (short_name.length() > 24) {
    short_name = short_name.substring(0, 22) + "..";
  }
  return short_name;
}

class Button {
  String label;
  float x, y, w, h;
  int fontSize;

  Button(String label, float x, float y, int fontSize) {
    this.label = label;
    this.x = x;
    this.y = y;
    this.fontSize = fontSize;
  }

  void display() {
    fill(200);
    stroke(0);
    rect(x, y, w, h);
    fill(0);
    textAlign(CENTER, CENTER);
    textSize(fontSize);
    text(label, x + w / 2, y + h / 2);
  }

  boolean isClicked(float mx, float my) {
    return mx > x && mx < x + w && my > y && my < y + h;
  }
}

