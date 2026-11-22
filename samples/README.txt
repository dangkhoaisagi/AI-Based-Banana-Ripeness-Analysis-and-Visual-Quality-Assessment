18 ẢNH CHUỐI CÓ NHÃN ĐỂ KIỂM THỬ WEBSITE


CẤU TRÚC
do_chin/xanh/: 3 ảnh, nhãn nguồn unripe.
do_chin/chin/: 3 ảnh, nhãn nguồn ripe.
do_chin/qua_chin/: 3 ảnh, nhãn nguồn overripe.
chat_luong_quy_doi/tot/: 3 ảnh, nhãn nguồn ripe.
chat_luong_quy_doi/dom/: 3 ảnh, nhãn nguồn overripe.
chat_luong_quy_doi/thoi/: 3 ảnh, nhãn nguồn rotten.

THÔNG TIN NHÃN
Nhãn nguồn lấy từ thư mục lớp do người cung cấp dataset đặt. Nhãn chất lượng được quy đổi đúng theo notebook người dùng: ripe -> tot, overripe -> dom, rotten -> thoi. Chưa xác minh độc lập rằng ripe luôn là tốt hoặc overripe luôn là đốm. Không dùng nhãn quy đổi để kết luận an toàn thực phẩm.

Thứ tự đầu ra theo notebook người dùng:
- Model độ chín: ["chin", "qua_chin", "xanh"].
- Model chất lượng quy đổi: ["dom", "thoi", "tot"].

NGUỒN
Độ chín: Banana Ripeness Classification Dataset, S.M. Shahriar.
https://www.kaggle.com/datasets/shahriar26s/banana-ripeness-classification-dataset
Giấy phép dataset do người cung cấp công bố qua Kaggle: Apache 2.0.

Chất lượng quy đổi: Banalyzer - Banana Ripeness Classification Dataset, Charles C R.
https://www.kaggle.com/datasets/iamchaarles/banalyzer-banana-ripeness-classification-dataset
Giấy phép dataset do người cung cấp công bố qua Kaggle: MIT.

labels.json ghi đường dẫn gốc, nhãn nguồn, nhãn quy đổi, phiên bản dataset, kích thước, mã SHA-256 và nguồn của từng ảnh. Giữ thông tin nguồn/giấy phép khi sử dụng hoặc phân phối lại.

PHẠM VI KIỂM THỬ
Các ảnh là file riêng lẻ tải nguyên byte từ dataset, chỉ đổi tên file để dễ dùng; không cắt từ ảnh ghép, không chỉnh sửa và không tạo bằng AI. Bản thân dataset có thể đã resize hoặc xử lý ảnh trước đó; không khẳng định đây là ảnh nguyên bản từ máy ảnh.

Các file được chọn từ thư mục test của dataset gốc. Chưa xác minh trùng lặp với tập người dùng đã dùng để train/validation/test hoặc giữa các dataset. Gói này phục vụ kiểm tra chức năng và đối chiếu nhãn; không phải tập đánh giá độc lập và không dùng để công bố một Accuracy mới. Bổ sung ảnh tự chụp chưa dùng huấn luyện nếu muốn đánh giá khả năng áp dụng thực tế.

Không cần dùng model RGB/phổ để kiểm thử phần chất lượng. Phần chất lượng cần model Banalyzer đã được huấn luyện theo ba nhãn quy đổi tương ứng.
