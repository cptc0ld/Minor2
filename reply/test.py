from reply.params import hp
import torch
from reply.model import Net
from pytorch_pretrained_bert import BertTokenizer
from collections import OrderedDict
from colorama import Fore, Style
import pickle, re

import argparse

def prepare_inputs(context, tokenizer):
    '''context
    context: I love you. [SEP] Sorry, I hate you.
    '''
    tokens = tokenizer.tokenize(context)
    tokens = tokenizer.convert_tokens_to_ids(tokens)[-hp.max_span+2:]
    tokens = [101] + tokens + [102]
    # print(f"{Fore.LIGHTBLACK_EX}context:{tokenizer.convert_ids_to_tokens(tokens)}{Style.RESET_ALL}")
    tokens = torch.LongTensor(tokens)
    tokens = tokens.unsqueeze(0) # (1, T)
    tokens = tokens.to("cuda")
    
    return tokens

def suggest(context, tokenizer, model, idx2phr):
    x = prepare_inputs(context, tokenizer)
    model.eval()
    with torch.no_grad():
        _, y_hat, y_hat_prob = model(x)
        y_hat = y_hat.cpu().numpy().flatten()  # (3)
        y_hat_prob = y_hat_prob.cpu().numpy().flatten()  # (3)
        y_hat_prob = [round(each, 2) for each in y_hat_prob]
        preds = [idx2phr.get(h, "None") for h in y_hat]
        preds = " | ".join(preds)
        print(f"{Fore.BLUE}{preds}{Style.RESET_ALL}")
        print(f"{y_hat_prob}{Style.RESET_ALL}")

def pred_ans(msg):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

    print("Wait... loading model")
    ckpt = "C:\\Users\\dheer\\OneDrive\\Documents\\Vscode\\Minor2\\reply\\log\\9500_ACC0.33.pt"
    model = Net(hp.n_classes)
    model = model.cuda()
    ckpt = torch.load(ckpt)
    # model.load_state_dict(ckpt)

    # ckpt = OrderedDict([(k.replace("module.", "").replace("LayerNorm.weight", "LayerNorm.gamma").replace("LayerNorm.bias", "LayerNorm.beta"), v) for k, v in ckpt.items()])
    ckpt = OrderedDict([(k.replace("module.", ""), v) for k, v in ckpt.items()])
    model.load_state_dict(ckpt)
    print("Model loaded.")

    print("# loading dictionaries ..")
    idx2phr = pickle.load(open(hp.idx2phr, 'rb'))
    suggest(msg, tokenizer, model, idx2phr)
