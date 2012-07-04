require 'redmine'

Redmine::Plugin.register :redmine_repos do
  name 'Redmine Repos plugin'
  author 'Swetha V,Piyush Bansal'
  description 'This is a plugin for Redmine'
  version '0.0.1'

  permission :new_repo, { :repos => [:create] }
  permission :repos, { :repos => [:index] }, :public => true
  menu :project_menu, :repos, { :controller => 'repos', :action => 'index' }, :caption => 'Repositories', :after => :activity, :param => :project_id
end
