# TJSlides 教學
### 教你如何使用 Markdown
by tonytonyjan
http://tjslides.herokuapp.com/slides/2

## 什麼是 TJSlides
TJSlides 是個利用純文字產生簡報的工具  
能將 [Markdown] 標記語言
轉換成為 [reveal.js] 支援的格式
### 意思就是
要使用 TJSlides 你得學一些 [Markdown] 語法

## 如何判定分頁？
在 [Markdown] 下標有六個大小：

    # Heading 1
    ## Heading 2
    ### Heading 3
    #### Heading 4
    ##### Heading 5
    ###### Heading 6

其中 `#` 和 `##` 用於分頁判定  
`#` 通常是首頁大標，`##` 則是一般標題

## 標題範例
    ## 標題 2 範例
### 標題 3 範例
    ### 標題 3 範例
#### 標題 4 範例
    #### 標題 4 範例
##### 標題 5 範例
    ##### 標題 5 範例
###### 標題 6 範例
    ###### 標題 6 範例

## 無序清單
*   第一行
*   第二行
*   第三行

---

    *   第一行
    *   第二行
    *   第三行

## 有序清單
1.  第一行
2.  第二行
3.  第三行

---

    1.  第一行
    2.  第二行
    3.  第三行

## 引用
>   敏感和敏銳不一樣，前者是感性的極端，
>   可以用來罵人；後者是理性的極端，
>   可以用來稱讚人。敏感的人大多不快樂，
>   敏銳的人則大多知人知心。

by 大兜

---

    >   敏感和敏銳不一樣，前者是感性的極端，
    >   可以用來罵人；後者是理性的極端，
    >   可以用來稱讚人。敏感的人大多不快樂，
    >   敏銳的人則大多知人知心。

## 連結
### 有兩種方式：
[直接標注](http://tjslides.herokuapp.com)：

    [直接標注](http://tjslides.herokuapp.com)（title 可略）:

[標籤標注][id]（title 可略）：
[id]: http://tjslides.herokuapp.com "Title"

    [標籤標注][id]（title 可略）：
    然後在任何地方定義標籤：
    [id]: http://tjslides.herokuapp.com "Title"


## 插入圖片
和連結一樣但是多了一個驚嘆號

![Tony Jian](http://i.imgur.com/ShxGX.jpg "Tony Jian")

直接標注（title 可略）:

    ![Tony Jian](http://i.imgur.com/ShxGX.jpg "Tony Jian")

標籤標注:
    [id]: http://tonytonyjan.github.com/images/ice-ball.jpg "Title"


## 程式碼
需要空下** 4 個空白**或** 1 個 tab**：

    class Fixnum
      def prime?
        ('1' * self) !~ /^1?$|^(11+?)\1+$/
      end
    end

---

    需要空下** 4 個空白**或** 1 個 tab**：
    
        class Fixnum
          def prime?
            ('1' * self) !~ /^1?$|^(11+?)\1+$/
          end
        end

程式碼會自動判斷並上色
    
支援的語言請參考 [highlight.js](http://softwaremaniacs.org/soft/highlight/en/description/)

# 讚美 reveal.js

## 瀏覽所有頁面
按一下 **ESC** 可以進入綜覽模式！

## 跳到任一頁
你可以在每張投影片之間做跳躍：

[像這樣](#/3)

    你可以在每張投影片之間做跳躍：
    
    [像這樣](#/3)

# 感謝閱讀！
### 趕快<a href="/users/sign_in" target="_top">登入</a>然後<a href="/slides/new" target="_top">試試看</a>吧！
有任何反饋也請到<a href="/board" target="_top">這裡</a>留下你的訊息