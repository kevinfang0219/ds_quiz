import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ds_quiz.settings')
django.setup()

from quiz.models import Question, Choice

# 這裡總共 20 題！
hash_questions = [
    # --- 原本的 15 題 ---
    {
        "text": "何謂「雜湊表」？",
        "choices": ["一種將元素依大小順序排列的資料結構", "一種按照樹狀結構排列的資料結構", "一種將鍵值依雜湊函數計算索引或位址的資料結構", "一種根據「先進先出」規則的資料結構"],
        "correct_index": 2
    },
    {
        "text": "電腦科學領域中，「雜湊表」的主要目的為何？",
        "choices": ["依大小順序排列儲存資料", "依壓縮的格式儲存資料", "提供有效率的資料存取", "對資料進行數學運算"],
        "correct_index": 2
    },
    {
        "text": "「雜湊表」的基本操作為何？",
        "choices": ["搜尋", "插入", "刪除", "以上皆是"],
        "correct_index": 3
    },
    {
        "text": "下列哪種資料結構在搜尋單筆資料時最有效率？",
        "choices": ["鏈結串列", "堆疊", "佇列", "二元搜尋樹", "雜湊表"],
        "correct_index": 4
    },
    {
        "text": "「雜湊表」的搜尋，在最壞情況下的時間複雜度為何？",
        "choices": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
        "correct_index": 2
    },
    {
        "text": "「雜湊表」的插入，在最壞情況下的時間複雜度為何？",
        "choices": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
        "correct_index": 2
    },
    {
        "text": "下列何者是造成「雜湊表」碰撞問題的主要原因？",
        "choices": ["兩筆鍵值的雜湊函數值相等", "雜湊表已滿", "雜湊函數計算錯誤", "兩筆鍵值相同"],
        "correct_index": 0
    },
    {
        "text": "下列方法中，何者不是用來解決「雜湊表」的碰撞問題？",
        "choices": ["線性探測 (Linear Probing)", "二次探測 (Quadratic Probing)", "雙重雜湊 (Double Hashing)", "指數探測 (Exponential Probing)"],
        "correct_index": 3
    },
    {
        "text": "何謂「雙重雜湊」 (Double Hashing)？",
        "choices": ["使用兩個不同的雜湊函數，以解決碰撞問題", "若相同的鍵值，則使用兩次雜湊函數", "一種加密的方法", "使得雜湊表的大小變為原來兩倍的方法"],
        "correct_index": 0
    },
    {
        "text": "雜湊表中的「負載因子」(Load Factor) 是如何計算的？",
        "choices": ["雜湊表大小除以元素個數", "元素個數除以雜湊表大小", "發生碰撞的次數除以元素個數", "發生碰撞的次數除以雜湊表大小"],
        "correct_index": 1
    },
    {
        "text": "在解決雜湊碰撞時，「鏈結法」(Chaining) 主要使用哪種資料結構來儲存發生碰撞的元素？",
        "choices": ["佇列 (Queue)", "堆疊 (Stack)", "鏈結串列 (Linked List)", "二元樹 (Binary Tree)"],
        "correct_index": 2
    },
    {
        "text": "當使用「線性探測」(Linear Probing) 來解決碰撞時，最容易發生下列哪種缺點？",
        "choices": ["主聚集 (Primary Clustering) 現象", "次聚集 (Secondary Clustering) 現象", "記憶體洩漏 (Memory Leak)", "堆疊溢位 (Stack Overflow)"],
        "correct_index": 0
    },
    {
        "text": "一個良好的「雜湊函數」(Hash Function) 最應該具備什麼特性？",
        "choices": ["計算過程越複雜越好", "輸出的索引值應該盡可能集中在某些特定位置", "能夠均勻地將鍵值分佈在整個雜湊表中", "必須使用隨機亂數產生器來決定位址"],
        "correct_index": 2
    },
    {
        "text": "當雜湊表的負載因子過高，導致效能嚴重下降時，通常會採取什麼操作來解決？",
        "choices": ["隨機刪除部分資料", "重新雜湊 (Rehashing)，擴大表格並重新計算所有元素位置", "將雜湊表轉換為一般的陣列", "更改雜湊函數但不改變表格大小"],
        "correct_index": 1
    },
    {
        "text": "在最佳情況下（沒有發生任何碰撞），雜湊表搜尋一筆資料的時間複雜度為何？",
        "choices": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
        "correct_index": 0
    },
    
    # --- 全新加入的 5 題 ---
    {
        "text": "在使用「線性探測 (Linear Probing)」處理碰撞的雜湊表中，刪除資料時通常會採取什麼特殊做法？",
        "choices": ["直接將該位置清空", "將陣列後面的元素全部往前移", "標記為「已刪除」(Tombstone) 而不真正清空", "將該位置的值設為 0"],
        "correct_index": 2
    },
    {
        "text": "何謂「完美雜湊函數 (Perfect Hash Function)」？",
        "choices": ["計算速度最快的雜湊函數", "能將所有的鍵值對應到陣列中且「完全不發生碰撞」的雜湊函數", "能夠自動擴充雜湊表大小的函數", "具有加密保護功能的雜湊函數"],
        "correct_index": 1
    },
    {
        "text": "假設雜湊表大小為 7，雜湊函數為 H(x) = x mod 7，使用「線性探測」解決碰撞。依序插入 10, 17, 24，請問 24 最後會被放在哪個索引位置？",
        "choices": ["3", "4", "5", "6"],
        "correct_index": 2
    },
    {
        "text": "在選擇雜湊表大小 (Table Size) 時，為了減少碰撞並讓資料均勻分布，通常會建議將大小設定為下列何種數字？",
        "choices": ["質數 (Prime Number)", "偶數", "2的次方數 (Power of 2)", "10的倍數"],
        "correct_index": 0
    },
    {
        "text": "關於雜湊表中的「開放定址法 (Open Addressing)」，下列敘述何者正確？",
        "choices": ["所有元素都儲存在雜湊表本身的陣列內，不使用額外的鏈結指標", "發生碰撞時，會將元素放入鏈結串列中", "記憶體空間的利用率永遠比鏈結法 (Chaining) 差", "負載因子 (Load Factor) 可以大於 1"],
        "correct_index": 0
    }
]

def seed_data():
    print("清空舊題目中...")
    Question.objects.all().delete()
    
    print("開始匯入 20 題雜湊表題目...")
    for q_data in hash_questions:
        question = Question.objects.create(text=q_data["text"])
        for i, choice_text in enumerate(q_data["choices"]):
            is_correct = (i == q_data["correct_index"])
            Choice.objects.create(
                question=question,
                text=choice_text,
                is_correct=is_correct
            )
        print(f"成功匯入：{question.text}")
    print("✨ 20 題全部匯入完成！題庫已擴充！")

if __name__ == '__main__':
    seed_data()