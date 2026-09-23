from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker
import os
DB_URL=os.getenv("DATABASE_URL","sqlite:///./impact_lab.db")
engine=create_engine(DB_URL, connect_args={"check_same_thread":False} if DB_URL.startswith("sqlite") else {})
metadata=MetaData()
def table(name, cols): return Table(name, metadata, *[Column(c[0],c[1],**c[2]) for c in cols])
dim_country=table("dim_country",[("country_id",Integer,{},),("country_code",String(8),{"primary_key":True}),("country_name",String(80),{})])
dim_program=table("dim_program",[("program_id",Integer,{"primary_key":True}),("program_code",String(20),{}),("program_name",String(100),{})])
dim_site=table("dim_site",[("site_id",Integer,{"primary_key":True}),("site_code",String(30),{}),("country_code",String(8),{}),("program_id",Integer,{})])
dim_indicator=table("dim_indicator",[("indicator_id",Integer,{"primary_key":True}),("indicator_code",String(30),{}),("indicator_name",String(100),{})])
dim_funding_source=table("dim_funding_source",[("funding_source_id",Integer,{"primary_key":True}),("funding_code",String(30),{}),("funding_name",String(100),{})])
dim_reporting_period=table("dim_reporting_period",[("period_id",Integer,{"primary_key":True}),("period_start",Date,{}),("period_label",String(20),{})])
fact_enrollment=table("fact_enrollment",[("record_id",Integer,{"primary_key":True}),("site_id",Integer,{}),("period_id",Integer,{}),("enrolled",Integer,{}),("updated_at",DateTime,{}),("status",String(20),{})])
fact_program_outcomes=table("fact_program_outcomes",[("record_id",Integer,{"primary_key":True}),("site_id",Integer,{}),("period_id",Integer,{}),("completion_rate",Float,{}),("attendance_rate",Float,{}),("updated_at",DateTime,{})])
fact_site_progress=table("fact_site_progress",[("record_id",Integer,{"primary_key":True}),("site_id",Integer,{}),("period_id",Integer,{}),("milestones",Integer,{}),("progress_pct",Float,{})])
fact_funding_allocation=table("fact_funding_allocation",[("record_id",Integer,{"primary_key":True}),("funding_source_id",Integer,{}),("program_id",Integer,{}),("site_id",Integer,{}),("amount",Float,{}),("allocation_status",String(20),{})])
fact_data_submission=table("fact_data_submission",[("record_id",Integer,{"primary_key":True}),("site_id",Integer,{}),("period_id",Integer,{}),("submitted_at",DateTime,{}),("is_complete",Boolean,{}),("is_stale",Boolean,{})])
fact_data_quality_issue=table("fact_data_quality_issue",[("issue_id",Integer,{"primary_key":True}),("table_name",String(60),{}),("record_id",Integer,{}),("dimension",String(30),{}),("issue_type",String(60),{}),("severity",String(15),{}),("description",String(255),{}),("detected_at",DateTime,{})])
fact_data_refresh=table("fact_data_refresh",[("refresh_id",Integer,{"primary_key":True}),("table_name",String(60),{}),("refreshed_at",DateTime,{}),("row_count",Integer,{})])
fact_ad_hoc_request=table("fact_ad_hoc_request",[("request_id",Integer,{"primary_key":True}),("request_type",String(60),{}),("requested_at",DateTime,{}),("status",String(20),{})])
fact_migration_reconciliation=table("fact_migration_reconciliation",[("reconciliation_id",Integer,{"primary_key":True}),("entity_type",String(40),{}),("source_key",String(80),{}),("target_key",String(80),{}),("match_status",String(20),{}),("difference_reason",String(160),{})])
ALL_TABLES=[dim_country,dim_program,dim_site,dim_indicator,dim_funding_source,dim_reporting_period,fact_enrollment,fact_program_outcomes,fact_site_progress,fact_funding_allocation,fact_data_submission,fact_data_quality_issue,fact_data_refresh,fact_ad_hoc_request,fact_migration_reconciliation]
def create_schema(): metadata.create_all(engine)
