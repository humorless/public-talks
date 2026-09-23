# KM Project Review

請 review "knowledge manager" 這個專案，簡稱 KM。

## context

KM 是 for 一家台灣的鋼鐵業的企業使用，該企業員工人數有 800 人，但是，公司的白領人數可能只有 250 人上下。由 knowledge manager 管理的 unstructured data，初期的 data 只有過往的公司規章，約 500 分文件。

KM 專案是用來做企業內部的「非結構化資料」的知識管理，預計會放入許多的非結構化資料，格式可能很多種，而初期認定的作法是：「先無論如何轉成 pdf，再來做後續的處理。」

最初負責開發的工程師沒有做過此類型的專案，考慮到之後可能會要一直微調與修改，就選用了 HayStack，因為判斷如此可能相對容易修改、調整。

## KM project

KM 專案目前由 2 個 repo 構成 (都在本資料夾下)：

- `km-inferencing-api/`
- `data-ingestion-pipeline/`

KM 專案對應的架構設計是 "Inference-service-architecture-Pipeline Architecture.jpg"

## zero-base thinking design

這邊採取 zero-base thinking 的思考，如果這件事完全還沒有開始，可能會怎麼做？於是，我也設計了一個 spec 文件，是如果由我來做，預計採用的作法。spec 文件是 `levinrag-SPEC.md`。

## tasks

1. 請先**獨立思考** KM 的 purpose，由此推導合理的設計、「應該」的規格、架構。**此階段先不要參考 `levinrag-SPEC.md`，以避免受到參考設計的影響。**

2. review KM 的現況，讀 2 個 repo 的程式碼，推理而得出：KM 的規格、架構。

3. review zero-base thinking design，讀 `levinrag-SPEC.md`，推理而得出：levinrag 的規格、架構。

4. 本 review 採用以下對 Rich Hickey「simple」的工作定義：
   「things that are not inherently connected should not be artificially coupled」，也就是避免把本來可以分離的 concerns / dimensions 綁在一起。
      若用上述的 simple definition 來分析 KM 的 2 repos 與 levinrag，各有哪些地方 not simple？

5. 基於先前的分析，試列舉出 3~5 種 use cases or situations，是 KM 在不大改架構的前提之下，很難處理得好的、或是很有可能會失敗的。

6. 綜合前面的分析，如果考慮 KM 下一步的 architecture evolution ，不預設必須繼續沿用目前 KM 的 architecture，請評估以下可能路徑： 
  - 繼續以 KM 目前的 architecture 為基礎進行修改
  - 直接改採 levinrag
  - 保留 KM 的部分 components / architecture，與 levinrag 組合
  - 其他你認為合理的 architecture evolution path

## review methodology

在 review 過程中，請明確區分：

- **Observed**：從 code、configuration、architecture diagram、spec 或其他文件中直接觀察到的事實。
- **Inferred**：根據上述 evidence 推理而得出的結論。
- **Assumed**：基於 domain/context 而採用、但未能從專案本身直接驗證的假設。
- **Recommended**：reviewer 基於分析所提出的建議。

不要將 inference、assumption 或 recommendation 描述成既有系統的事實。

將 1, 2, 3, 4, 5, 6 的答案都輸出成 markdown 文件。