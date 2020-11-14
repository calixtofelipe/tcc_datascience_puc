class PreparaTest():
    def __init__(self, ds_validacao):
        self.ds_validacao = ds_validacao
        
    def preparation(self):
        preprocess = PreProcessing(self.ds_validacao)
        dataset_validacao = preprocess.processar()
        input_ids = []
        for sentence in dataset_validacao['nome_produto_processed']:
            encoded_sent = tokenizer.encode(sentence, add_special_tokens = True) #[CLS] - INICIO FRASE E [SEP] FINAL FRASE
            input_ids.append(encoded_sent)
        MAX_LEN = 52
        input_pad = pad_sequences(input_ids, maxlen=MAX_LEN, dtype='long', value=0, truncating="post", padding='post')
        
        attention_masks = []
        for sent in input_pad:
                att_mask  = [int(token_id > 0) for token_id in sent]
                attention_masks.append(att_mask) 

        le = preprocessing.LabelEncoder()
        labels = le.fit_transform(dataset_validacao['categoria'])
        dataset_validacao['categoria_encoded'] = labels



        val_inputs = torch.tensor(input_pad)

        val_labels = torch.tensor(dataset_validacao['categoria_encoded'].values)

        val_masks = torch.tensor(attention_masks)
        
        batch_size = 32
        val_data = TensorDataset(val_inputs, val_masks, val_labels)
        val_sampler = SequentialSampler(val_data)
        val_dataloader = DataLoader(val_data, sampler=val_sampler, batch_size=batch_size)
        
        return val_dataloader