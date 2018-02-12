from datetime import datetime
import sys
class Report:
    def __init__(self,inputfile,outputfile,percentilefile):
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.percentilefile = percentilefile
        self.name_zipcode_set = set()
        self.dict_rec_zc_year_amt= dict()
        self.dict_rec_zc_year_count = dict()
        self.dict_rec_zc_year_dollar = dict()
    
    
    def get_percentile(self,recp_yr_zc,percentile):
        total_count = len(self.dict_rec_zc_year_dollar[recp_yr_zc])
        rank = float(percentile) * float(total_count) / float(100)
        if( round(rank) < 1):
            rank = 1
            return self.dict_rec_zc_year_dollar[recp_yr_zc][rank-1]
        else:
            rank = int(round(rank))
            return self.dict_rec_zc_year_dollar[recp_yr_zc][rank-1]
    
    
    def check_valid_record(self,rec):
        
        if( len(rec[15]) == 0 and (len(rec[13]) == 8 and (self.check_date1(rec[13]) or self.check_date2(rec[13]))) and len(rec[10]) > 5 and  len(rec[7]) != 0 and len(rec[0]) != 0 and len(rec[14]) != 0):
            
            return True

        return False
    
    def check_date1(self,date_text):
        
        try:
            datetime.strptime(date_text, '%m%d%Y')
            b = True
        except ValueError:
            b = False
        
        return b

    def check_date2(self,date_text):
        try:
            datetime.strptime(date_text, '%m%d%Y')
            b = True
        except ValueError:
            b = False
        
        return b

    
    
    def put_rec_year_zipcode_amt(self,recp_yr_zc,rec):
        if recp_yr_zc in self.dict_rec_zc_year_amt:
            self.dict_rec_zc_year_amt[recp_yr_zc] = int(self.dict_rec_zc_year_amt[recp_yr_zc]) + int(rec[14])
        
        else:
            self.dict_rec_zc_year_amt[recp_yr_zc] = int(rec[14])

    def put_rec_year_zipcode_count(self,recp_yr_zc):
        if recp_yr_zc in self.dict_rec_zc_year_count:
            self.dict_rec_zc_year_count[recp_yr_zc] = self.dict_rec_zc_year_count[recp_yr_zc] + 1
        else:
                self.dict_rec_zc_year_count[recp_yr_zc] = 1

    def put_rec_year_zipcode_year_dollar(self,recp_yr_zc,rec):
            if recp_yr_zc in self.dict_rec_zc_year_dollar:
                self.dict_rec_zc_year_dollar[recp_yr_zc].append(rec[14])
            else:
                self.dict_rec_zc_year_dollar[recp_yr_zc] = [rec[14]]
    

    
    def get_records(self):
        
        with open(self.percentilefile,'r') as p:
            percentile = p.read()
        
        with open(self.outputfile,'w') as fw:
            with open(self.inputfile,'r') as fr:
                for line in fr:
                    rec = line.strip().split('|')
                    
                    if(self.check_valid_record(rec)):
                        
                        
                        
                        zipcode_name = str(rec[10][:5]) + str(rec[7]) # zipcode name
                        recp_yr_zc = str(rec[0])+' '+str(rec[13][-4:]) +  ' ' + str(rec[10][:5]) #recipient year zipcode
                        
                        #inserting into dictionaries
                        if(zipcode_name in self.name_zipcode_set):
                            
                            self.put_rec_year_zipcode_amt(recp_yr_zc,rec)
                            
                            self.put_rec_year_zipcode_count(recp_yr_zc)
                            
                            self.put_rec_year_zipcode_year_dollar(recp_yr_zc,rec)
                            
                            
                            perc = self.get_percentile(recp_yr_zc,percentile)
                            
                            #Output Format:recipientId|zipcode|year|percentile|amount|countZipcode
                            output = str(rec[0]) + '|' + str(rec[10][:5]) +'|' + str(rec[13][-4:]) +'|' + str(perc) +'|'+ str(self.dict_rec_zc_year_amt[recp_yr_zc]) + '|' + str(self.dict_rec_zc_year_count[recp_yr_zc])
                            
                            fw.write(output +'\n')
                        
                        else:
                            self.name_zipcode_set.add(zipcode_name)





if __name__ == "__main__":
    
    inputfile = '/Users/aishwaryapatil/Desktop/itcont.txt'
    percentilefile = '/Users/aishwaryapatil/Desktop/percentile.txt'
    outputfile = '/Users/aishwaryapatil/Desktop/records.txt'
    c = Report(inputfile,outputfile,percentilefile)
    c.get_records()
