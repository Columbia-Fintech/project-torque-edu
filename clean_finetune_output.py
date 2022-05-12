import os

def clean_file(path, infile_name):
    infile = open(path+infile_name,'r')
    outfile = open(path+"clean_"+infile_name, 'w')
    lines = infile.readlines()
    qa_dict = dict()
    q = ""
    a = ""
    for line in lines:
        # replacements
        line = line.replace("\\u00a0","")
        line = line.replace("\\u201c","\"")
        line = line.replace("\\u201d","\"")
        line = line.replace("\\u2019","'")

        if line[0] == "'":
            # question line
            q = line[0:-3]
        elif line[0] == '}':
            q = ""
            a = ""
        else:
            # find answer
            line = line.strip()
            if line.find("\"text\":")>=0:
                a = line[9:]
                if a[-1] == "\"":
                    a = a[:-1]
                a = a.strip()
                a = a.rstrip()

                if len(q)>0:
                    if len(a)>0:
                        qa_dict[q] ="'"+a+"'"
                        outfile.write(q+": '"+a+"'\n")
                        print(q, qa_dict[q])
                        q = ""
                        a = ""

if __name__ == '__main__':
    for n in (10,20,50,100,200):
        clean_file("./curie_finetune/","output_curie_"+str(n)+".txt")

    print(os.getcwd())
    clean_file("./davinci_finetune/","output_davinci_100.txt")
