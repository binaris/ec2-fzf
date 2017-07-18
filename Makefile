.PHONY: deploy
deploy:
	sls deploy -s eu-central-1 -r eu-central-1
	sls deploy -s us-east-1 -r us-east-1

.PHONY: deploy_function
deploy_function:
	sls deploy function -f discover_instances -s us-east-1 -r us-east-1
	sls deploy function -f discover_instances -s eu-central-1 -r eu-central-1

.PHONY: run_local
run_local:
	sls invoke local -f discover_instances

.PHONY: run_eu_central_1
run_eu_central_1:
	sls invoke -f discover_instances -s eu-central-1 -r eu-central-1

.PHONY: run_us_east_1
run_us_east_1:
	sls invoke -f discover_instances -s us-east-1 -r us-east-1
