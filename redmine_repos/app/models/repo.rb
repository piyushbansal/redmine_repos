class Repo < ActiveRecord::Base
  validates_presence_of :reponame
  validates_presence_of :description
    
  def manage(action, repotype, lab_id, reponame)
    sub_cmd = "~/repoadmin.py "+action+" "+repotype+" "+lab_id+" "+reponame
   # command = 'ssh svnadmin@devel "'+sub_cmd+'"'
    response = `#{sub_cmd}`
    j = ActiveSupport::JSON
    response = j.decode(response)
  end
end
