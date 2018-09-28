from custom_tools import *

class Selene_Job:
    def __init__(self, job_id):
        self.job_id = job_id
        self.local_job_directory_path = 'ssh_remote_jobs/job_' + str(job_id)
        self.selene_ssh_remote_jobs_path = 'guilminp@selene.mskcc.org:/home/guilminp/impact-annotator/analysis/prediction/ssh_remote_jobs'
        self.selene_job_directory_path = self.selene_ssh_remote_jobs_path + '/job_' + str(job_id)
        
        self.make_local_job_directory_()
        

    def make_local_job_directory_(self):
        print('➞ mkdir ' + self.local_job_directory_path)
        ! mkdir {self.local_job_directory_path}
    

    def run(self):
        print('➞ scp ' + self.local_job_directory_path + ' to ' + self.selene_ssh_remote_jobs_path)
        ! scp -r {self.local_job_directory_path} {self.selene_ssh_remote_jobs_path}

        test = 'echo "➞ Logged in $PWD on $HOSTNAME"; \
                \
                echo "➞ Load ~/.bash_profile"; \
                source ~/.bash_profile; \
                export LSF_ENVDIR=/common/lsf/conf; export LSF_SERVERDIR=/common/lsf/9.1/linux2.6-glibc2.3-x86_64/etc; \
                \
                echo "➞ Work on impact-annotator_env python virtualenv"; \
                workon impact-annotator_env; \
                \
                cd ~/impact-annotator/analysis/prediction/ssh_remote_jobs/job_' + str(self.job_id) + '; \
                echo "➞ Launch job in $PWD"; \
                bsub -o job_output.txt -We 20 "python script.py"'

        ! ssh guilminp@selene.mskcc.org '{test}'
    

    def get_results(self):        
        test = 'cd ~/impact-annotator/analysis/prediction/ssh_remote_jobs/job_' + str(self.job_id) + '; \
               [ -e metrics.pkl ] && echo "yes" || echo "no"'
            
        file_found = ! ssh guilminp@selene.mskcc.org '{test}'
        file_found = file_found[0]

        if file_found == "yes":
            print_md("✅ <span style='color:green'>Job \< " + str(self.job_id) + " \> finished !</span>\n")
            print('➞ scp ' + self.selene_job_directory_path + ' documents to ' + self.local_job_directory_path)
            ! scp -r {self.selene_job_directory_path}/metrics.csv {self.local_job_directory_path}
            ! scp -r {self.selene_job_directory_path}/job_output.txt {self.local_job_directory_path}
            print('➞ Load metrics.pkl in pandas dataframe')
            self.metrics = pd.read_csv(self.local_job_directory_path + '/metrics.pkl', sep = ',', low_memory = False)
            
            return(self.metrics)
        else:
            print_md("⚠️ <span style='color:red'>Job \< " + str(self.job_id) + " \> doesn't exist or is not done yet.</span>\n")