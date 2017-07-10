.PHONY: deploy
deploy:
	sls deploy

.PHONY: deploy_function
deploy_function:
	sls deploy function -f discover_instances

.PHONY: run_local
run_local:
	sls invoke local -f discover_instances

.PHONY: run_remote
run_remote:
	sls invoke -f discover_instances
