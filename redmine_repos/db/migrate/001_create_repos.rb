class CreateRepos < ActiveRecord::Migration
  def self.up
    create_table :repos do |t|
      t.column :lab_id, :string
      t.column :reponame, :string
      t.column :description, :string
      t.column :created_on, :timestamp
      t.column :repotype, :string
    end
  end

  def self.down
    drop_table :repos
  end
end
