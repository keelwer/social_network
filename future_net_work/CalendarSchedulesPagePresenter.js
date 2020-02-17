import React, {Component} from 'react';
import CheckForTrickTable from './CheckForTrickTable';
import MarketTabContainer from '../containers/MarketTabContainer';
import {Scrollbars} from 'react-custom-scrollbars';
import './styles/tab.css';
import ReactModal from 'react-modal';
import _ from 'lodash';
import './styles/modal.css';
import './styles/buttons.css';

class CalendarSchedulesPagePresenter extends Component {
  state = {
        isModalOpened: false,
        currentRole: {},
        currentActionType: {},
        currentAvailableActions: [],
        scheduleCalendarDel: null,
        isDeleteModalOpened: false,
  }
  applyFilter = (filters) => {
    this.props.changePage(1);
    this.props.changeFilters(filters);
    this.props.getCalendarSchedules(this.props.market, 1, filters);
  }
  changeValues = (newValues, oldValues) => {
    this.props.changeValues(this.props.market, newValues, oldValues)
  }
  changePage = (page) => {
    this.props.changePage(page);
    this.props.getCalendarSchedules(this.props.market, page, this.props.filters);
  }
  render() {
    let props = this.props;
    return (<div className="tab-segment">
      <div className="headline-segment">
        <p className="safran-headline">{props.title}</p>
      </div>
      <Scrollbars style={{
          height: '100%'
        }} autoWidth="autoWidth">
        <div className="text-logs-segment">
          <CheckForTrickTable
            visible={!props.isFetching}
            currentPage={props.page}
            numPages={props.numPages}
            changePage={this.changePage}
            columns={[
              {
                key: 'fromDate',
                header: 'Начало интервала',
                dataBinding: 'fromDate',
                type: 'date',
              },
              {
                key: 'toDate',
                header: 'Конец интервала',
                dataBinding: 'toDate',
                type: 'date'
              },
              {
                key: 'todo',
                header: 'Воздействие',
                dataBinding: 'todo',
                type: 'select',
                choices: [
                  {
                    value: 'R',
                    text: 'Работать'
                  },
                  {
                    value: 'S',
                    text: 'Отдыхать'
                  }
                ]
              }
            ]} filters={[
              {
                key: 'fromDate',
                type: 'date',
                header: 'С',
                defaultValue: new Date(+new Date() - 1000*60*60*24)
              }, {
                key: 'toDate',
                type: 'date',
                header: 'По'
              },
              {
                key: 'todo',
                header: 'Воздействие',
                type: 'select',
                defaultValue: 'R'
              }
            ]}
            applyFilterCallback={this.applyFilter}
            applyChanges={this.changeValues}
            data={props.calendarSchedules}
            isDeletable={true}
            deleteCallback={(schedule) => {
            this.setState({scheduleCalendarDel: schedule, isDeleteModalOpened: true})
            }}
            canCreateNewRows={true}
            createCallback={(schedule) => {this.props.createValue(this.props.market, schedule)}}
          />
        </div>
                <ReactModal isOpen={this.state.isDeleteModalOpened} style={{
                    content: {
                        backgroundColor: 'white',
                        top: '50%',
                        left: '50%',
                        right: 'auto',
                        bottom: 'auto',
                        marginRight: '-50%',
                        transform: 'translate(-50%, -50%)',
                        width: '485px',
                        height: '200px',
                        padding: '0'
                    }
                }}>
                <div className="c4t-users-modal">
                    <div>
                            <p className="safran-modal-title">Предупреждение</p>
                        </div>
                        <div className="safran-modal-content">
                            {<p>Вы уверены, что хотите удалить интервал календарного плана работы?</p>}
                        </div>
                        <div className="modal-bottom">
                            <button className="c4t-button" onClick={() => {
                                this.props.deleteValue(this.props.market, this.state.scheduleCalendarDel)
                                this.setState({isDeleteModalOpened: false})
                            }}>Да
                            </button>
                            <button className="c4t-button" style={{
                                marginLeft: '5px'
                            }} onClick={() => this.setState({isDeleteModalOpened: false})}>Нет
                            </button>
                        </div>
                </div>
        </ReactModal>
      </Scrollbars>
      <MarketTabContainer/>
    </div>)
  }
}

export default CalendarSchedulesPagePresenter;
