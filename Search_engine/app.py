from flask import Flask, render_template
from flask import request

from fse import IndexedLineDocument
from fse.models import base_s2v
from vncorenlp import VnCoreNLP

app = Flask(__name__, static_folder='static')
wsgi_app = app.wsgi_app

# app.config['TESTING'] = True
# app.testing = True
# app.config["TEMPLATES_AUTO_RELOAD"] = True

annotator = VnCoreNLP("H:/Vietnamese word representations/VncoreNLP_lite/VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m')
model_path = "H:/Vietnamese word representations/Data/tuoitre_sent2vec/tuoitre_vec"
model = base_s2v.BaseSentence2VecModel.load(model_path)
print("loading model")

title_path = "H:/Vietnamese word representations/Data/tuoitre_title_des_link_tokenized.csv "
# title_path = "H:/Vietnamese word representations/Data/tuoitre_title_link_with_separator_tokenized.csv"
doc = IndexedLineDocument(title_path)
print("loading title")


@app.route('/')
def home():
    return render_template('notgoogle.html')


@app.route('/result', methods=['GET', 'POST'])
def search():
    output_result = []
    query = None
    if request.method == "POST":
        query = request.values['search'] or ''
        try:
            if "_" not in query:
                query = annotator.tokenize(query)
                if len(query) == 1:
                    query = query[0]
                else:
                    print("")
            else:
                query = [query]

        except Exception as e:
            raise Exception("Something went wrong: msg = %s, query = %s." % (e, query))
        print(query)
        print('query = ' + str(query))

        try:
            # dummy
            # output = [('tai nạn giao thông', 'tai nạn giao thông'), ('tai nạn giao thông', 'tai nạn giao thông'),
            #           ('tai nạn giao thông', 'tai nạn giao thông'), ('tai nạn giao thông', 'tai nạn giao thông'), ]

            output = []
            sim_list = model.sv.similar_by_sentence(query, model=model, indexable=doc)

            for wordsim in sim_list:
                result = wordsim[0].split(",|_sep_|,")

                # wordsim[2] ~ cosine similarity
                result[0] = result[0].replace('_', ' ')
                print(result[0])
                result[1] = result[1].replace('_', ' ')
                print(result[1])

                # title = result[0].replace('_', ' ')
                # hyper_link = result[1]
                output.append(result)
            output_result = output
        except Exception as e:
            output = 'Err: %s, Not found query = %s' % (e, query)
            output_result.append(output)

        print(f'output = {output_result}')

    return render_template('result.html',
                           query=query,
                           value=output_result
                           )


# @app.route("/result")
# def query_result():
#     output_result = []
#     try:
#         output = []
#         sim_list = model.sv.similar_by_sentence(query, model=model, indexable=doc)
#         for wordsimilar in sim_list:
#             result = wordsimilar[0].split(",_|_separator_|_,")
#             title = result[0]
#             hyper_link = result[1]
#             output.append(result)
#         output_result = output
#     except Exception as e:
#         output = 'Err: %s, Not found query = %s' % (e, query)
#         output_result = output
#     return render_template('notgoogle.html', output=output_result)

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True, use_reloader=False, port=8089, host='0.0.0.0')
