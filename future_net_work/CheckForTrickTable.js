import {connect} from 'react-redux';
import React, {Component} from 'react';
import TimePicker from './react-time-picker';
import DatePicker from './react-date-picker';
import DateTimePicker from 'react-datetime-picker';
import ToggleButton from './ToggleButton';
import ToggleGroup from './ToggleGroup';
import {WrongFilterTypeError} from '../exceptions';
import Loader from 'react-loader-spinner';
import lArrow from '../static/Fleft.png';
import llArrow from '../static/FFleft.png';
import rArrow from '../static/Fright.png';
import rrArrow from '../static/FFright.png';
import moment from 'moment';
import _ from 'lodash';
import {saveFilters} from '../ducks/filters';
import './styles/table.css';
import './styles/caption.css';
import './styles/buttons.css';

class CheckForTrickTable extends Component {

  state = {
    filterValues: {},
    createValues: {},
    changedDataKey: null,
    isCreatingRecord: false,
    changedData: {}
  }
  isButtonClicked = false;

  isSavedFiltersValid = (savedFilters) => {
    for (const key in savedFilters) {
      if (!(this.props.filters.map((filter) => filter.key)).includes(key)) {
        return false
      }
    }
    return true
  }

  saveFiltersToSessionStorage = (filtersToSave) => {
    let filters = Object.assign({}, filtersToSave)
    for (const key in filters) {
      if (filters[key] instanceof Date) {
        filters[key] = moment(filters[key]).format('DD.MM.YYYY HH:mm:ss')
      }
    }
    sessionStorage.setItem('__filters',JSON.stringify(filters))
  }

  readFiltersFromSessionStorage = () => {
    let filters = JSON.parse(sessionStorage.getItem('__filters'))
    for (const key in filters) {
      if (moment(filters[key], 'DD.MM.YYYY HH:mm:ss').isValid()) {
        filters[key] = moment(filters[key], 'DD.MM.YYYY HH:mm:ss').toDate()
      }
    }
    return filters
  }

  constructor(props) {
    super(props);
    const filters = this.readFiltersFromSessionStorage()
    if (props.filters !== undefined) {
      if (filters !== undefined && filters !== null && this.isSavedFiltersValid(filters))
      {
        this.state.filterValues = filters;
      }
      else {
        props.filters.forEach((filter) => {
          if (filter.defaultValue !== undefined) {
            this.state.filterValues[filter.key] = filter.defaultValue;
          } else {
            this.state.filterValues[filter.key] = getInitInputValue(filter.type);
          }
        })
      }
    }
    this.props.applyFilterCallback && this.props.applyFilterCallback(convertInputValues(this.state.filterValues, this.state.filterMode, this.props.filters))
    props.columns.forEach((column) => {
      this.state.createValues[column.key] = getInitInputValue(column.type);
    })
  }
  render() {
    let columns = this.props.columns;
    let filters = this.props.filters;
    if (filters !== undefined) {
      let headers = filters.map((filter) => filter.header);
    }
    let data = this.props.data;
    let rowKeyBinding = this.props.rowKeyBinding;
    if (this.props.visible === false) {
      return (<div className="filter-center"><Loader type="ThreeDots" color="blue" height={80} width={80}/></div>)
    }
    return (<div>
      {
        this.props.canCreateNewRows && <button className="c4t-create-record-button" onClick={() => this.setState({
              isCreatingRecord: !this.state.isCreatingRecord
            })}>{
              this.state.isCreatingRecord
                ? "x Вернуться к фильтру"
                : "+ Создать запись"
            }</button>
      }
      <table className="safran-table" border="1">
        <thead>
          {
            (this.props.canCreateNewRows || this.props.filters !== undefined) && <tr>
                {
                  !this.state.isCreatingRecord && this.props.filters !== undefined && <th colspan="100%" className="filter-header-row">
                      <div className="filter-header offset-filter">
                        <form className="filters" onSubmit={(e) => {
                            e.preventDefault()
                            this.props.applyFilterCallback(convertInputValues(this.state.filterValues, this.state.filterMode, filters))
                            this.saveFiltersToSessionStorage(this.state.filterValues)
                          }}>
                          {
                            filters.map((filter) => {
                              let filterColumn = columns.find((column) => filter.key === column.key);
                              let choices = undefined;
                              if (filterColumn !== undefined) {
                                choices = filterColumn.choices;
                              }
                              return getInput(filter.type, this.state.filterValues[filter.key], filter.header, (value) => {
                                this.setState({filterValues: Object.assign({}, this.state.filterValues, {
                                    [filter.key]: value
                                  })})
                              }, choices)
                            })
                          }
                          <div className="vertical-line"/>
                          <input type="submit" value="Применить" className="c4t-button"></input>
                        </form>
                      </div>
                    </th>
                }
                {
                  this.state.isCreatingRecord && <th colspan="100%" className="create-record-header-row">
                      <div className="filter-header-edit">
                        <div className="filter-modes">
                          <p className="safran-filter-text">Создать запись</p>
                        </div>
                        <form className="filters" onSubmit={(e) => {
                            e.preventDefault()
                            this.props.createCallback(convertInputValues(this.state.createValues, null, columns))
                          }}>
                          {
                            columns.map((column) => {
                              return getInput(column.type, this.state.createValues[column.key], column.header, (value) => {
                                this.setState({createValues: Object.assign({}, this.state.createValues, {
                                    [column.key]: value
                                  })})
                              }, column.choices, false)
                            })
                          }
                          <input type="submit" value="Создать" className="c4t-button"></input>
                        </form>
                      </div>
                    </th>
                }
              </tr>
          }
          <tr>
            {columns.map((column) => <th>{column.header}</th>)}
          </tr>
        </thead>
        {
          this.props.currentPage !== undefined && <tfoot>
              <tr>
                <th colspan="100%">
                  <div className="page-footer-row">
                    <TablePaginator changePage={this.props.changePage} numPages={(
                        this.props.numPages === undefined)
                        ? 1
                        : this.props.numPages} currentPage={(
                        this.props.currentPage === undefined)
                        ? 1
                        : this.props.currentPage}/>
                  </div>
                </th>
              </tr>
            </tfoot>
        }
        <tbody>
          {
            data.map((item, i) => <tr onClick={() => {
                if (this.state.changedDataKey === null || this.state.changedDataKey === undefined || this.state.changedDataKey !== i) {
                  let changedData = Object.assign({}, item)
                  this.setState({changedDataKey: i, changedData: changedData})
                }
                this.props.onRowClick && this.props.onRowClick(item);
              }}>
              {
                columns.map(
                  (column, j) => this.state.changedDataKey === i && (!column.readOnly || this.props.isDeletable)
                  ? <td>
                    <div className="table-row-inputs">
                      {
                        !column.readOnly
                          ? getInput(column.type, _.get(this.state.changedData, column.dataBinding), null, (value) => {
                            this.setState({changedData: Object.assign({}, this.state.changedData, {
                                [column.dataBinding]: value
                              })})
                          }, column.choices, false)
                          : (
                            (column.cellFunction)
                            ? column.cellFunction(item)
                            : _.get(item, column.dataBinding))
                      }
                      {
                        (j + 1 === columns.length) && <div>
                            {
                              !column.readOnly && <button type="button" className="c4t-table-button" onClick={() => {
                                    this.setState({changedDataKey: null})
                                    this.props.applyChanges(this.state.changedData, item)
                                  }}>Сохранить</button>
                            }
                            {
                              !column.readOnly && <button type="button" className="c4t-table-button" onClick={() => {
                                    this.setState({changedDataKey: null})
                                  }}>Отменить</button>
                            }
                            {
                              this.props.isDeletable && <button type="button" className="c4t-table-button" onClick={() => {
                                    this.setState({changedDataKey: null})
                                    this.props.deleteCallback(item)
                                  }}>Удалить</button>
                            }
                          </div>
                      }</div>
                  </td>
                  : <td>{
                      column.choices === undefined
                        ? (column.cellFunction)
                          ? column.cellFunction(item)
                          : _.get(item, column.dataBinding)
                        : column.choices.find((choice) => choice.value === _.get(item, column.dataBinding) || choice.text === _.get(item, column.dataBinding)) === undefined
                          ? ""
                          : column.choices.find((choice) => choice.value === _.get(item, column.dataBinding) || choice.text === _.get(item, column.dataBinding)).text
                    }</td>)
              }
            </tr>)
          }
        </tbody>
      </table>
    </div>)
  }
}

const mapStateToProps = (state) => {
  return {savedFilters: state.filters.savedFilters}
}

const mapDispatchToProps = (dispatch) => {
  return {

  }
}

export default connect(mapStateToProps, mapDispatchToProps)(CheckForTrickTable);

class TablePaginator extends Component {
  componentDidUpdate(prevProps) {
    if (prevProps.currentPage !== this.props.currentPage) {
      this.setState({inputPage: this.props.currentPage})
    }
  }
  state = {
    inputPage: this.props.currentPage
  }
  render() {
    let props = this.props;
    return (<div className="page-footer">
      <button className="prev-page-button" type="button" onClick={() => props.changePage(1)}><img src={llArrow} alt="&lt;&lt;"/></button>
      <button className="prev-page-button" type="button" onClick={() => {
          if (props.currentPage > 1) {
            props.changePage(props.currentPage - 1)
          }
        }}><img src={lArrow} alt="&lt;"/></button>
      <input className="page-input" type="text" value={(
          this.state.inputPage === undefined)
          ? 1
          : this.state.inputPage} onChange={(event) => this.setState({inputPage: getChangedText(event)})}/>
      <button className="next-page-button" type="button" onClick={() => {
          if (props.currentPage < props.numPages) {
            props.changePage(props.currentPage + 1)
          }
        }}><img src={rArrow} alt="&gt;"/></button>
      <button className="next-page-button" type="button" onClick={() => props.changePage(props.numPages)}><img src={rrArrow} alt="&gt;&gt;"/></button>
      <p className="safran-page-caption">из {props.numPages}</p>
      <button className="page-submit-button" type="button" onClick={() => {
          if (parseInt(this.state.inputPage) >= 1 && parseInt(this.state.inputPage) <= props.numPages) {
            props.changePage(parseInt(this.state.inputPage))
          }
        }}>Перейти</button>
    </div>)
  }
}


function getInput(inputType, value, header, onChangeCallback, choices = [], allInChoices = true) {
  if (inputType === 'date') {
    if (value !== null) {
      var date = moment(value, "DD.MM.YYYY").toDate();
    } else {
      var date = null;
    }
    return (<div className="datetime-filter">
      {header && <p className="safran-filter-caption">{header}</p>}
      <DatePicker locale="ru-RU" value={date} onChange={(date) => {
          if (date !== null) {
            onChangeCallback(moment(date).format("DD.MM.YYYY"))
          } else {
            onChangeCallback(null)
          }
        }}/>
    </div>)
//  } else if (inputType === 'time') {
//    return (<div className="datetime-filter">
//      {header && <p className="safran-filter-caption">{header}</p>}
//      <TimePicker locale="ru-RU" value={value} maxDetail="second" onChange={onChangeCallback} clearIcon={null} clockIcon={null}/>
//    </div>)
//  } else if (inputType === 'datetime') {
//    return (<div className="datetime-filter">
//      {header && <p className="safran-filter-caption">{header}</p>}
//      <DateTimePicker locale="ru-RU" value={value} onChange={onChangeCallback}/>
//    </div>)
//  } else if (inputType === 'text') {
//    return (<div className="text-filter">
//      {header && <p className="safran-top-filter-caption">{header}</p>}
//      <input className="c4t-input" value={value} onChange={(event) => onChangeCallback(getChangedText(event))}/>
//    </div>)
  } else if (inputType === 'select') {
    return (<div className="text-filter">
      {header && <p className="safran-top-filter-caption">{header}</p>}
      <select className="c4t-select" onChange={(event) => onChangeCallback(getChangedText(event))}>
        {allInChoices && <option value="">Все</option>}
        <option value={option.value} selected={optionsState == option.value}>{option.label}</option>
        {choices.map(choice => (<option selected={value === choice.value || value === choice.text} value={choice.value}>{choice.text}</option>))}
      </select>
    </div>)
//  } else if (inputType === 'checkbox') {
//    return (<div className="text-filter">
//      {header && <p className="safran-top-filter-caption">{header}</p>}
//      <input type="checkbox" checked={value} onChange={(event) => onChangeCallback(getChangedText(event))}></input>
//    </div>)
//  } else if (inputType === 'password') {
//      return (<div className="text-filter">
//          {header && <p className="safran-top-filter-caption">{header}</p>}
//          <input type="password" className="c4t-input" value={value} onChange={(event) => onChangeCallback(getChangedText(event))}/>
//      </div>)
//  } else {
//    throw new WrongFilterTypeError(inputType);
//  }
}

function getChangedText(event) {
  return  event.target.type === 'checkbox' ? event.target.checked : event.target.value;
}

function getInitInputValue(inputType) {
  if (isInputDateOrTime(inputType)) {
    return new Date();
  } else if (inputType === 'text' || inputType === 'select' || inputType === 'password') {
    return "";
  } else if (inputType === 'checkbox') {
    return false
  } else {
    throw new WrongFilterTypeError(inputType);
  }
}

function isInputDateOrTime(inputType) {
  return inputType === 'date' || inputType === 'time' || inputType === 'datetime';
}

function convertInputValues(inputValues, filterMode, inputs) {
  let convertedFilterValues = Object.assign({}, inputValues);
  for (let key in inputValues) {
    let value = inputValues[key];
    let inputType = inputs.find((filter) => filter.key === key).type;
    if (value !== null) {
      if (inputType === 'date') {
        value = (value instanceof Date)
          ? value.toLocaleDateString("ru-RU")
          : value;
      } else if (inputType === 'time') {
        value = (value instanceof Date)
          ? value.toLocaleTimeString("ru-RU")
          : value;
      } else if (inputType === 'datetime') {
        value = (value instanceof Date)
          ? value.toLocaleString("ru-RU")
          : value;
      }
    } else {
      value = "";
    }
    convertedFilterValues[key] = value;
  }
  if (filterMode !== null || filterMode !== undefined)
    convertedFilterValues["filterMode"] = filterMode;
  return convertedFilterValues;
}
