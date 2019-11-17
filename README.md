# time-series

### Install libraries
```python
pip3 install -r requirements.txt
```

### Run web app
```python
python3 -m dashboard.app
```

### About web app
Web app được xây dựng dựa trên Dash framework (https://plot.ly/dash/), 
nên có thể vào user guide của dash để xem cách hoạt động của web app (https://dash.plot.ly/getting-started)

Data khi load vào web app sẽ qua các file local hoặc kết nối với database, và sẽ được load đầu tiên trước khi web app chạy.

Về cơ bản, web app sẽ có layout được chia thành nhiều phần, mỗi phần được đánh dấu bằng một id riêng. 
Mỗi "mảng" layout sẽ thực hiện 1 chức năng như plot hoặc show table, và khi thay đổi trên 1 layout, ta có thể kết nối để tự động thay đổi trên layout khác.
Ví dụ: khi lựa chọn 1 vùng các điểm trên 1 scatter plot, ta có thể liệt kê các điểm đấy ra dưới dạng 1 table.

Khi muốn tùy chỉnh web app, ta có thể thay đổi phần layout, mỗi mảng layout hoạt động như thế nào, hoặc thay đổi các kết nối giữa các layout (callbacks).
