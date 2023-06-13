from flask import Flask, render_template, request
import pandas as pd
from sklearn import preprocessing
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        file = request.files['file']
        if file.filename == '':
            pesan_error = "tidak ada file dataset yang diupload"
            return render_template('index.html', pesan_error=pesan_error)
        
        try:
            dataset, dataset_dinormalisasi = dataset_normal(file)
            return render_template('index.html', dataset=dataset, dataset_dinormalisasi=dataset_dinormalisasi)
        except KeyError:
            pesan_error = "mohon ikuti aturan penulisan kolom"
            return render_template('index.html', pesan_error=pesan_error)
        except OSError:
            pesan_error = "File yang diupload bukan sebuah dataset"
            return render_template('index.html', pesan_error=pesan_error)
        except Exception as e:
            pesan_error = f"Terjadi kesalahan yang tidak terduga: {str(e)}"
            return render_template('index.html', pesan_error=pesan_error)
    
    return render_template('index.html')


def dataset_normal(file):
    try:
        extensi_file = os.path.splitext(file.filename)[1]
        
        if extensi_file == '.csv':
            csv_data = pd.read_csv(file)
        elif extensi_file == '.xlsx':
            csv_data = pd.read_excel(file)
        elif extensi_file == '.json':
            csv_data = pd.read_json(file)
        else:
            raise ValueError("Format dataset tidak didukung")
    except Exception as e:
        raise OSError(f"Gagal membaca file dataset: {str(e)}")

    
    aturan_kolom = ['kolom 1', 'kolom 2', 'kolom 3']
    if not set(aturan_kolom).issubset(csv_data.columns):
        raise KeyError()

    array = csv_data.values
    X = array[:, 0:3]
    Y = array[:, 3]

    dataset = pd.DataFrame({'kolom 1': X[:, 0], 'kolom 2': X[:, 1], 'kolom 3': X[:, 2]})
    print("Dataset sebelum dinormalisasi:")
    print(dataset.head(15))

    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1))
    data = min_max_scaler.fit_transform(X)
    dataset_dinormalisasi = pd.DataFrame({'kolom 1': data[:, 0], 'kolom 2': data[:, 1], 'kolom 3': data[:, 2], 'status': Y})

    print("Dataset setelah dinormalisasi:")
    print(dataset_dinormalisasi.head(15))

    return dataset.head(15).to_html(index=False), dataset_dinormalisasi.head(15).to_html(index=False)





if __name__ == '__main__':
    app.run(debug=True)
