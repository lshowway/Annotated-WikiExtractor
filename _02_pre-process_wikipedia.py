import json
import os

def statics(dir):
    files = os.listdir(dir)
    samples_count, total_length = 0, 0
    total_sentence_num, total_sentence_length = 0, 0

    url_set = set()
    anchor_set = set()
    uri_set = set()
    entity_set = set()



    for file in files:
        with open(os.path.join(dir, file), encoding='utf-8') as f:
            for line in f:
                x = json.loads(line)
                if not x:
                    continue
                id = x['id']
                url = x['url']

                url_set.add(url)
                entity_set.add(url)

                text = x['text']
                total_length += len(text.split())

                sentences_list = text.split('\n')
                total_sentence_num += len(sentences_list)
                for sentence in sentences_list:
                    total_sentence_length += len(sentence.split())

                annotations = x['annotations']
                samples_count += 1
                for ann in annotations:
                    surface_form = ann['surface_form']
                    uri = ann['uri']

                    anchor_set.add(surface_form)
                    uri_set.add(uri)
                    entity_set.add(uri)

                    offset = ann['offset']
                    assert text[offset: offset + len(surface_form)] == surface_form

    print('the total number of samples is: ', samples_count)
    print('the average number of word in each document is: ', total_length / samples_count)
    print('the total number of url is: ', len(url_set))
    print('the total number of anchor is: ', len(anchor_set))
    print('the total number of linked entity is: ', len(uri_set))
    print('the total number of entity is: ', len(entity_set))

    print('the total number of sentences is: ', total_sentence_num)
    print('the averge length of sentences is: ', total_sentence_length / total_sentence_num)


def add_identifier(dir, write_dir):
    if not os.path.exists(write_dir):
        os.makedirs(write_dir)

    files = os.listdir(dir)

    for file in files:
        print(file)
        with open(os.path.join(write_dir, file), 'w', encoding='utf-8') as fw:
            with open(os.path.join(dir, file), encoding='utf-8') as f:
                for line in f:

                    json_line = {}

                    x = json.loads(line)
                    if not x:
                        continue
                    url = x['url']
                    title = url.split('/')[-1]
                    text = x['text']

                    annotations = reversed(x['annotations'])
                    last_offset = -1
                    new_annotations = {}
                    for ann in annotations:
                        surface_form = ann['surface_form']
                        uri = ann['uri']

                        offset = ann['offset']

                        if last_offset != -1:
                            assert offset < last_offset
                        last_offset = offset
                        t = text[offset: offset + len(surface_form)]
                        assert t == surface_form
                        text = text[:offset] + '<s>' + surface_form + '</s>' + text[offset+len(surface_form):]
                        new_annotations[surface_form] = uri

                    json_line['title'] = title
                    sentences = [a for i, a in enumerate(text.split('\n')) if i != 0]
                    text = ' '.join(sentences)
                    json_line['text'] = text
                    json_line['annotation'] = new_annotations

                    json.dump(json_line, fw)
                    fw.write('\n')


def split_into_segments(dir, write_dir):
    if not os.path.exists(write_dir):
        os.makedirs(write_dir)

    files = os.listdir(dir)

    for file in files:
        with open(os.path.join(write_dir, file), 'w', encoding='utf-8') as fw:
            with open(os.path.join(dir, file), encoding='utf-8') as f:
                for line in f:

                    json_line = {}

                    x = json.loads(line)
                    title = x['title']
                    text = x['text']

                    json.dump(json_line, fw)
                    fw.write('\n')



if __name__ == "__main__":
    dir = "G:\D\MSRA\knowledge_aware\Annotated-WikiExtractor-master/annotated_wikiextractor\AA"
    write_dir = "G:\D\MSRA\knowledge_aware\Annotated-WikiExtractor-master/annotated_wikiextractor\BB"
    statics(dir)
    # add_identifier(dir, write_dir)